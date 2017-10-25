$(function(){
    $("#checkall").change(function(){
        if($(this). is(':checked')){
            $(".checkthis").prop('checked', true);
        }else{
            $(".checkthis").prop('checked', false);
        }
    })
})