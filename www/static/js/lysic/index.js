'use strict';
(function(Vue, global, axios){
    

    // Vue.use(ElementUI);
    var APIs = {
        searchSongs: '/api/search_songs'
    };

    var app = new Vue({
        delimiters: ['[[', ']]'],
        el: '#app',
        data: {
            search: '',
            title: '网易云音乐歌词下载工具',
            searchResults: []
        },
        methods: {
            searchHandle: function(){
                var keywords = this.search;
                if(keywords){
                    axios.get(APIs.searchSongs, {
                        params: {
                            keywords: keywords
                        }
                    }).then(function(res){
                        console.log(res)
                    }).then(function(err){
                        console.log(err)
                    })
                }
            }
        },
        mounted: function(){

        }
    })
})(Vue, window, axios);