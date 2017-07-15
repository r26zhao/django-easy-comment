/**
 * Created by Aaron Zhao on 2017/7/15.
 */
$(function () {
    var ckwidth = document.getElementById('cmt-form').offsetWidth;
            CKEDITOR.replace('id_content',{
                toolbar:[
                    ['Bold', 'Italic', 'Underline', 'Format', 'RemoveFormat'],
                    ['NumberedList', 'BulletedList'],
                    ['Blockquote', 'CodeSnippet'],
                    ['Image', 'Link', 'Unlink']
                ],
                width:ckwidth,
                height:150,
                extraPlugins:'codesnippet,prism,widget,lineutils,uploadimage'
            });
});
