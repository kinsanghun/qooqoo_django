function getDate(name, date, url){
    $.ajax({
        url : url,
        type : "GET",
        async : false,
        data : {
            "name": name,
            "date": date,
        },
        dataType : "json",
        contentType : "application/json",
        success : function(datas) {
            result = []
            for(data of datas){
                result.push(data["fields"]);
            }
        }
    });
    return result;

}
function settingModal(name, date, data){
    $("#formname").val(name);
    $("#formdate").val(date);
}
