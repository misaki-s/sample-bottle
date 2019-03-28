let tabs = document.querySelectorAll('input[type="radio"][name="tab_item"]');
Array.from(tabs, function (e) {
  // hash変更
  e.addEventListener('click', function (e) {
    location.hash = e.currentTarget.id;
  });
});
(function () {
  // 削除ボタンに確認メッセージを追加
  let btnDelete = document.querySelectorAll('.btn-delete');
  Array.from(btnDelete,  function(e) {
    console.log(e);
    e.addEventListener('click', function(e){
      if(window.confirm('削除しますか？')){
        return true;
      } else {
        e.preventDefault();
        return false;
      }
    });
  });

  // URLにハッシュがある場合、タブを切り替える。
  // console.log("set hash");
  let hash = location.hash;
  if(hash){
    document.querySelector(hash).setAttribute('checked', true);
  }

  // ページロード時に検索にフォーカスさせる。
  document.querySelector('.searchText').focus();
})();


