//Treeview 구현
extend: $(document).ready(function(event){
    $('.first-view').on('click', function(){
        //Bubble-Up 방지
        $('.second-view').click(function(event){
            event.stopPropagation();
        })

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

