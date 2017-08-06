/**
 * Created by Aaron Zhao on 2017/8/5.
 */
jQuery(function ($) {
        var blink = {
            title:document.title,
            step:0,
            timer:null,
            is_flashing:false,
            show:function () {
                var temp = blink.title;
                blink.timer = setInterval(function () {
                    blink.step++;
                    if (blink.step%2 == 1){
                        document.title = "【新消息】" + blink.title;
                    }
                    else {
                        document.title = "【　　　】" + blink.title;
                    }
                }, 1000);
            },
            clear:function () {
                if (blink.is_flashing){
                    clearInterval(blink.timer);
                    document.title = blink.title;
                    blink.is_flashing = false;
                    $(".live-notify-badge").text('');
                }
            }
        };
        function fetch_data() {
            $.get(
                "/notifications/api/unread_count/",
                function (data) {
                    if (data.unread_count > 0){
                        $(".live-notify-badge").text(data.unread_count);
                        clearInterval(blink.timer);
                        document.title = "【新消息】" + blink.title;
                        blink.is_flashing = true;
                        blink.show();
                    }
                    else {
                        blink.clear();
                    }
                }
            );
        }
        fetch_data();
        setInterval(fetch_data, 30000);
});