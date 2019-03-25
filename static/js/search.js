function mySubmit(el){
  let searchForm = document.querySelector(".searchForm");
  let searchText= document.querySelector(".searchText");
  // location.href = '/search/'+searchText.value;
  el.action = '/search/'+searchText.value;
  el.setAttribute('disabled', true);
  return false;
}
