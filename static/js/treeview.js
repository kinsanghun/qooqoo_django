//first-view = fv로 표기, 내비게이션 first view 카운트 만큼 리스트 생성
var fvList = [];
var firstViewCount = 0;

//클릭하면 해당 인덱스의 first-view의 값이 expand로 변함
function nodeUpdate(list, index){
    list[index] = 'expand';
}

//리스트 생성
function makeList(list, cnt){
    for(i=0; i<cnt; i++){
        list.push('collapse'); //초깃값은 collapse
    }
}

//Treeview 
$(document).ready(function(event){
    //click시 idx 정보 가져오기
    var idx = $(this).index();

    //firstview 갯수 세기
    firstViewCount = document.getElementsByClassName('first-view').length;

    makeList(fvList, firstViewCount);

    //토글기능
    $('.first-view').on('click', function(){
        //Bubble-Up 방지
        $('.second-view').click(function(event){
            event.stopPropagation();
        })

        // click시 리스트 업데이트
        nodeUpdate(fvList, idx);
        
        //클릭 시 슬라이드 및 아이콘 변경
        if($('.second-view', this).is(':visible')){
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
