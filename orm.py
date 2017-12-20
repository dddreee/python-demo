#!/user/bin/evv python3
# -*- coding: utf-8 -*-
import asyncio
import aiomysql, logging; logging.basicConfig(level=logging.INFO)

def log(sql, args=()):
    logging.info('SQL: {0} \r\n Args: {1}'.format(sql, args))


async def create_pool(loop, **kw):
    logging.info('create database connection pool....')
    global __pool
    __pool = await aiomysql.create_pool(
        host = kw.get('host', 'localhost'),
        port = kw.get('port', 8003),
        user = kw['user'],
        password = kw['password'],
        db = kw['db'],
        charset = kw.get('charset', 'uft8'),
        autocommit = kw.get('autocommit', True),
        maxsize = kw.get('maxsize', 10),
        minsize = kw.get('minsize', 1),
        loop = loop
        
    )

async def select(sql, args, size=None):
    log(sql, args)
    global __pool
    async with __pool as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:

            await cur.execute(sql.replace('?', '%s'), args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()

        logging.info('rows returned: {0}'.format(len(rs)))

        return rs

async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
    
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()

        except BaseException as e:
            if not autocommit:
                await conn.rollback()

            print(str(e))
            raise
        
        return affected

def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)

class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
    
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '{0}'".format(key))
        
    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug("using default value for {0}: {1}".format(key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        ''' find objects by where clause '''
        sql = [cls.__select__]

        if where:
            sql.append('where')
            sql.append(where)
        
        if args is None:
            args = []

        orderBy = kw.get('orderBy', None)

        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                sql.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: {0}'.format(limit))
        
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        ''' find number by select and where '''
        sql = ['select {0} _num_ from `{1}`'.format(selectField, cls.__table__)]

        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    async def find(cls, pk):
        ''' find object by primary key '''
        rs = await select('{0} where `{1}`=?'.format(cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))

        rows = await execute(self.__insert__, args)

        if rows != 1:
            logging.warn('failed to insert record: affected rows: {0}'.format(rows))

    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))

        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: {0}'.format(rows))
        
    async def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = await execute(self.__delete__, args)

        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: {0}'.format(rows))




class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<{0}, {1}:{2}>'.format(self.__class__.__name__, self.column_type, self.name)

class StringField(Field):
    ''' 映射varchar的StringField '''
    def __init__(self, name=None, primary_key=False, default=None, ddl="varchar(100)"):
        super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)

class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)

class FloatFlied(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)

class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # 清除Model类本身
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        # 获取table名称：
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: {0} (table: {1})'.format(name, tableName))

        # 获取所有Field和主键名
        mappings = dict()
        fields = []
        primaryKey = None

        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('  found mapping: {0} ==> {1}'.format(k, v))
                mappings[k] = v

                if v.primary_key:
                    # 找到主键
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: {0}'.format(k))
                    primaryKey = K

                else:
                    fields.append(k)
        if not primaryKey:
            raise RuntimeError('primary key not found')

        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))

        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey
        attrs['__fields__'] = fields
        # 构造默认的select，insert，update 和 delete语句
        attrs['__select__'] = 'select `{0}`, {1} from `{2}`'.format(primaryKey, ','.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `{0}` ({1}, `{2}`) values ({3})'.format(tableName, ','.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `{0}` set {1} where `{2}` = ?'.format(tableName, ','.join(map(lambda f: '`{0}`=?'.format(mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `{0}` where `{1}`=?'.format(tableName, primaryKey)

        return type.__new__(cls, name, bases, attrs)

    