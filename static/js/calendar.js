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


                $("#annual").val(d["annual"]);
                $("#dayoff").val(d["dayoff"]);

                $("#end").val(d["end"]);
                $("#start").val(d["start"]);

                $("#content").val(d["content"]);
                $("#extra").val(d["extra"]);

                $("#extra_type").val(d["extra"]);
                $("#working").val(d["working"]);
            }
        }
    });

}