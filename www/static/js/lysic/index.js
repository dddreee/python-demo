'use strict';
(function(Vue, global, axios){
    

    // Vue.use(ElementUI);
    var API = {
        searchSongs: '/api/search_songs',
        downloadLrc: '/api/download_lrc'
    };

    var app = new Vue({
        delimiters: ['[[', ']]'],
        el: '#app',
        data: {
            search: '',
            title: '网易云音乐歌词下载',
            params: {
                pageSize: 30,
                // pageCount: 0,
                total: 0,
                currentPage: 1,


            },
            searchResults: []
        },
        methods: {
            // 搜索框搜索是，@clock=searchHandle, 不带()时，会默认传入event对象
            searchHandle: function(page){
                
                var keywords = this.search;
                var self = this;
                if(keywords){
                    axios.get(API.searchSongs, {
                        params: {
                            keywords: keywords,
                            pageSize: self.params.pageSize,
                            page: page || self.params.currentPage
                        }
                    }).then(function(res){
                        self.searchResults = res.data.result.songs;
                        self.params.total = res.data.result.songCount;
                    }).then(function(err){
                        console.log(err)
                    })
                }
            },
            downloadLrc: function(row){

                return '/api/download_lrc?id=' + row.id + '&name=' + row.name;

            },
            artistsHandle: function(row){
                var artists = row.artists.map(function(artist){
                    return '<a target="_blank" href="https://music.163.com/#/artist?id='+ artist.id +'">'+ artist.name +'</a>';
                });

                return artists.join('/');

            },
            handleSizeChange: function(val){
                console.log(val)
            },
            handleCurrentChange: function(val){
                this.searchHandle(val)
            }
        },
        mounted: function(){

        }
    })
})(Vue, window, axios);