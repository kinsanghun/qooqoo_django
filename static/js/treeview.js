//first-view = fv로 표기, 내비게이션 first view 카운트 만큼 리스트 생성
var fvList = [];
var firstViewCount = 0;

//클릭하면 해당 인덱스의 first-view의 값이 expand로 변함
function nodeUpdate(list, index) {
    if(list[index] == 0) {
        list[index] = 1;
    }
    else {
        list[index] = 0;
    }
}

//리스트 생성
function makeList(list, cnt) {
    for (i = 0; i < cnt; i++) {
        list.push(0); //초깃값은 collapse
    }
}

//Treeview 
$(document).ready(function (event) {
    //firstview 갯수 세기
    firstViewCount = document.getElementsByClassName('first-view').length;

    if(localStorage.getItem("fvList")) {
        console.log("already used")
        fvList = localStorage["fvList"].split(",").map(Number);

        // List update
        for(var i=1; i <= fvList.length; i++){
            if(fvList[i-1] > 0) {
                var target = $('.first-view:nth-child('+i+') .second-view');
                target.removeClass('ic-open').addClass('ic-close');
                target.removeClass('ic-folder-open').addClass('ic-folder');
                target.show();
            }
        }
    }
    else {
        makeList(fvList, firstViewCount);
        localStorage.setItem("fvList", fvList);
    }

    //Bubble-Up 방지
    $('.second-view').click(function (event) {
        event.stopPropagation();
    })

    //토글기능
    $('.first-view').on('click', function (e) {
        var idx = $(this).index(); // click시 idx 정보 가져오기
        nodeUpdate(fvList, idx);
        localStorage["fvList"] = fvList;ㅈ

        //클릭 시 슬라이드 및 아이콘 변경
        if ($('.second-view', this).is(':visible')) {
            $('.ic16.ic-open', this).removeClass('ic-open').addClass('ic-close');
            $('.ic16.ic-folder-open', this).removeClass('ic-folder-open').addClass('ic-folder');
            $('.second-view', this).slideUp();
        } else {
            $('.ic16.ic-close', this).removeClass('ic-close').addClass('ic-open');
            $('.ic16.ic-folder', this).removeClass('ic-folder').addClass('ic-folder-open');
            $('.second-view', this).slideDown();
        }
    })
})
