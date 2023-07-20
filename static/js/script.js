$(function () {
console.log(1234567)

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        }
    });
    function update_info() {
        //var $el = $('#weather-container');
        const $el = $('#tmp-value')
        $.ajax({
            type: 'GET',                  //获得URL地址  ajax启动需要配置确定url位置
            url: $el.data('href'),        //变成update-info路由
            success: function (data) {    //请求成功返回data
                //$el.text(data.message)    //改变显示内容。变成data。message
                //$el.text('123456')
                //$el.text(data.temperature)
                //console.log(data.abc)
                //console.log('success')
                $('#tmp-value').text(data.temperature)
                $('#humi-value').text(data.humidity)
                $('#noise-value').text(data.noise)
                $('#illu-value').text(data.illumination)
                $('#wind-value').text(data.windvelocity)
                $('#pm25-value').text(data.pm2p5)

            }
        });
    }

    if ( $("#weather-container").length > 0 ) {  //jquery写法，判断页面当前有无元素  》0有元素进行服务器哦访问
       setInterval(update_info, 2000);            //每隔两秒调用一次  后端访问数据  set浏览器内置API
    }
    else{
        console.log(123456789)
    }

});
