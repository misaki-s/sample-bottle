let tabs = document.querySelectorAll('input[type="radio"][name="tab_item"]');
Array.from(tabs, function (e) {
  // hash変更
  e.addEventListener('click', function (e) {
    location.hash = e.currentTarget.id;
  });
});
(function () {
  console.log("set hash");
  let hash = location.hash;
  if(hash){
    document.querySelector(hash).setAttribute('checked', true);
  }

  document.querySelector('.searchText').focus();
})();


