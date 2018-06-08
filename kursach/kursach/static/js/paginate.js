  $(document).ready(function(){

var postsOnPage = 8;
var currentPage = 1;
var numberOfPages = Math.ceil($(".post").length /postsOnPage);


  $('#txt').html('Page '+currentPage+' of '+numberOfPages);

  paginate(currentPage,numberOfPages,postsOnPage);


$("#first").on('click',function(){
currentPage = 1;
paginate(currentPage,numberOfPages,postsOnPage);
});

$("#previous").on('click',function(){
  if(currentPage>1){currentPage--;}
paginate(currentPage,numberOfPages,postsOnPage);
});

$("#next").on('click',function(){
if(currentPage<numberOfPages){currentPage++;}
paginate(currentPage,numberOfPages,postsOnPage);
});

$("#last").on('click',function(){
currentPage = numberOfPages;
paginate(currentPage,numberOfPages,postsOnPage);
})
  });

var paginate = function(currentPage,numberOfPages,postsOnPage){

  var itemsToHide = $(".post").filter(":lt("+(currentPage-1)*postsOnPage+ ")");

  $.merge(itemsToHide, $(".post").filter(":gt("+((currentPage*postsOnPage) -1) + ")"));
  itemsToHide.hide();

  var itemsToShow =  $(".post").not(itemsToHide);
  itemsToShow.show();

  $('#txt').html('Page '+currentPage+' of '+numberOfPages);

};
