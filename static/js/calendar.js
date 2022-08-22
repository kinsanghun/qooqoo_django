function convertMinuitToTime(m) {
    let hour = parseInt(m / 60)
    let minuit
    if (m % 60) {
        minuit = toString(m % 60).padStart(2, "0")
    } else {
        minuit = "00"
    }

    return hour + ":" + minuit
}

function convertFloatToTime(f) {
    let mul = parseInt(f / 30)
    return 0.5 * mul
}

function getWorkDate(name, date, url) {
    $.ajax({
        url: url,
        type: "GET",
        data: {
            "name": name,
            "date": date,
        },
        dataType: "json",
        contentType: "application/json",
        success: function (datas) {
            if (datas.length) {

                let target = datas[0]["fields"];
                $("input[name=workDate]").val(target["date"]);
                $("input[name=workName]").val(target["name"]);
                $("input[name='workType']").each(function () {
                    if (target["worktype"] === $(this).val()) {
                        $(this).prop("checked", true);
                    }
                });
                $("input[name=workStart]").val(convertMinuitToTime(target["workstart"]));
                $("input[name=workEnd]").val(convertMinuitToTime(target["workend"]));
                $("input[name=breakTime]").val(convertFloatToTime(target["breaktime"]));
                $("input[name=workContent]").val(target["content"]);
            } else {

                $("input[name=workDate]").val(date);
                $("input[name=workName]").val(name);

                $("input[name='workType']").each(function () {
                    if ($(this).val() === "출근") {
                        $(this).prop("checked", true);
                    }
                });
                $("input[name=workStart]").val("10:00");
                $("input[name=workEnd]").val("22:00");
                //$("input[name=breakTime]").val(0);
                $("input[name=workContent]").val("");
                return
            }

        },
        error: function (datas) {
            console.log("!!!!!!!!!!!!");
        }
    });

}

function resetInputData(url) {
    let date = $("input[name=workDate]").val();
    let name = $("input[name=workName]").val();
    getWorkDate(name, date, url);
}