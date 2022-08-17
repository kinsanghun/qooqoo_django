//
function clearlist() {
    $(".data-body").remove();
}

function gridSetting(id, len) {
    $(id).css("display", "grid");
    $(id).css("grid-template-columns", "repeat(" + len.toString() + ", 1fr)");
    $(id).css("grid-template-rows", "1fr");
}

function formSetData(data, key) {
    $("#id").val(key);
    Object.keys(data).forEach(function (k) {
        console.log(k, data[k]);
        $("#" + k).val(data[k]);
    });
}

function getData(keyValue, url) {
    var result = "";
    $.ajax({
        url: url,
        type: "GET",
        async: false,
        data: {"key": keyValue},
        dataType: "json",
        contentType: "application/json",
        success: function (datas) {
            if (datas) {

                result = datas[0]["fields"];
            } else {

            }
        },
        error: function () {
            console.log('error');
        }
    });
    return result;
}

function printData(hc, id, headers, datas) {
    if (hc) {
        var h = "";
        for (header of headers) {
            h += "<div class='datas'>" + header + "</div>";
        }
        $(id).append("<div id='data-header' class='data-header'>" + h + "</div>");
        gridSetting('#data-header', headers.length);
    }
    var count = 1;
    for (data of datas) {
        var d = "";
        for (items of data) {
            d += "<div class='datas'>" + items + "</div>";
        }
        $(id).append("<div id='data-body' class='data-body'>" + d + "</div>");
        count++;
    }
    gridSetting('.data-body', headers.length);
}

function printDataImportColor(hc, id, headers, datas) {
    if (hc) {
        var h = "";
        for (header of headers) {
            h += "<div class='datas'>" + header + "</div>";
        }
        $(id).append("<div id='data-header' class='data-header'>" + h + "</div>");
        gridSetting('#data-header', headers.length);
    }
    var count = 1;
    for (data of datas) {
        var d = "";
        for (items of data) {
            d += "<div class='datas'>" + items + "</div>";
        }
        data[data.length - 2].split("-")[0]
        var y = new Date();
        console.log(y.getFullYear());
        if (parseInt(data[data.length - 2].split("-")[0]) < y.getFullYear())
            $(id).append("<div id='data-body' class='data-body bg-red'>" + d + "</div>");
        else if (data[data.length - 1] == 1)
            $(id).append("<div id='data-body' class='data-body bg-gray'>" + d + "</div>");
        else
            $(id).append("<div id='data-body' class='data-body'>" + d + "</div>");

        count++;
    }
    gridSetting('.data-body', headers.length);
}


function getDatesStartToLast(startDate, lastDate) {
    var regex = RegExp(/^\d{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$/);
    if (!(regex.test(startDate) && regex.test(lastDate))) return "Not Date Format";
    var result = [];
    var curDate = new Date(startDate);
    while (curDate <= new Date(lastDate)) {
        result.push(curDate.toISOString().split("T")[0]);
        curDate.setDate(curDate.getDate() + 1);
    }
    return result;
}

function getTradeValue(client, month, url) {
    $.ajax({
        url: url,
        type: "GET",
        async: false,
        data: {
            "client": client,
            "month": month,
        },
        dataType: "json",
        contentType: "application/json",
        success: function (datas) {
            result = []
            for (data of datas) {
                result.push(data["fields"]);
            }
        }
    });
    return result;
}

function copyPrice() {
    var price = $("#price").val();
    $("#pay").val(price);
}

function filter_data(datas, filter, index) {
    var filtered_data = [];
    for (data of datas) {
        if (filter.includes(data[index])) {
            filtered_data.push(data);
        }
    }
    return filtered_data;
}

function delete_data(id, db, url) {
    if (id > 0) location.href = url + "?id=" + id + "&database=" + db;
}