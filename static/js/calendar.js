function getDate(name, date, url){

    $("#formname").val(name);
    $("#formdate").val(date);
    $.ajax({
        url : url,
        type : "GET",
        data : {
            "name": name,
            "date": date,
        },
        dataType : "json",
        contentType : "application/json",
        success : function(datas) {
            for(data of datas){
                console.log(data["fields"]);
                var d = data["fields"];

                if(d["annual"] == 1){
                    $("#dayoff").prop("disabled", true);
                }
                $("#annual").val(d["annual"]);
                $("#dayoff").val(d["dayoff"]);

                $("#working").val(d["working"]);
                if(d["working"] == "조퇴"){
                    $("#start").prop("readonly", false);
                    $("#end").prop("readonly", false);
                }
                $("#end").val(d["end"]);
                $("#start").val(d["start"]);

                $("#content").val(d["content"]);
                if(d["extra"]){
                    $("#extra").val(d["extra"]);
                    $("#extra-type").val(d["extra_type"]);
                }
            }
        }
    });

}

