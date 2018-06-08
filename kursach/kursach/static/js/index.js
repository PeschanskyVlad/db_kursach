$(document).ready(function(){


    $.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
    });

function Calendar2(id, year, month) {
var Dlast = new Date(year,month+1,0).getDate(),
    D = new Date(year,month,Dlast),
    DNlast = new Date(D.getFullYear(),D.getMonth(),Dlast).getDay(),
    DNfirst = new Date(D.getFullYear(),D.getMonth(),1).getDay(),
    calendar = '<tr>',
    month=["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"];

if (DNfirst != 0) {
  for(var  i = 1; i < DNfirst; i++) calendar += '<td>';
}else{
  for(var  i = 0; i < 6; i++) calendar += '<td>';
}

for(var  i = 1; i <= Dlast; i++) {
  if (i == new Date().getDate() && D.getFullYear() == new Date().getFullYear() && D.getMonth() == new Date().getMonth()) {
      _my = D.getMonth() +1;
    calendar += '<td class="today">' + '<a href="/'+D.getFullYear()+'S'+_my+'S'+i+'">'+i+'</a>';
  }else{
       _my = D.getMonth() +1;
    calendar += '<td>' + '<a href="/day/'+D.getFullYear()+'S'+_my+'S'+i+'">'+i+'';
  }
  if (new Date(D.getFullYear(),D.getMonth(),i).getDay() == 0) {
    calendar += '<tr>';
  }
}
for(var  i = DNlast; i < 7; i++) calendar += '<td>&nbsp;';
document.querySelector('#'+id+' tbody').innerHTML = calendar;
document.querySelector('#'+id+' thead td:nth-child(2)').innerHTML = month[D.getMonth()] +' '+ D.getFullYear();
document.querySelector('#'+id+' thead td:nth-child(2)').dataset.month = D.getMonth();
document.querySelector('#'+id+' thead td:nth-child(2)').dataset.year = D.getFullYear();
if (document.querySelectorAll('#'+id+' tbody tr').length < 6) {  // чтобы при перелистывании месяцев не "подпрыгивала" вся страница, добавляется ряд пустых клеток. Итог: всегда 6 строк для цифр
    document.querySelector('#'+id+' tbody').innerHTML += '<tr><td>&nbsp;<td>&nbsp;<td>&nbsp;<td>&nbsp;<td>&nbsp;<td>&nbsp;<td>&nbsp;';
}
}
Calendar2("calendar2", new Date().getFullYear(), new Date().getMonth());
// переключатель минус месяц
document.querySelector('#calendar2 thead tr:nth-child(1) td:nth-child(1)').onclick = function() {
  Calendar2("calendar2", document.querySelector('#calendar2 thead td:nth-child(2)').dataset.year, parseFloat(document.querySelector('#calendar2 thead td:nth-child(2)').dataset.month)-1);
}
// переключатель плюс месяц
document.querySelector('#calendar2 thead tr:nth-child(1) td:nth-child(3)').onclick = function() {
  Calendar2("calendar2", document.querySelector('#calendar2 thead td:nth-child(2)').dataset.year, parseFloat(document.querySelector('#calendar2 thead td:nth-child(2)').dataset.month)+1);
}



    $( "#confirm_button_u" ).click(function() {

        $.ajax({
        url: "/api/crawl/",
        method : "POST",
        type: "POST",
        data: {
            target: "ukra"
        } ,
        success: function (resp) {
          if (resp.error) {
                alert("Error");
                return;
            }

            var state = {
                crawlingStatus: null,
                data: null,
                taskID: null,
                statusInterval: 1
            };

            state.taskID = resp.task_id;
            state.crawlingStatus = resp.status;
            state.statusInterval = setInterval(checkCrawlStatus, 2000, state);

        },
        error: function(jqXHR, textStatus, errorThrown) {
           console.log(textStatus, errorThrown);
        }
        });

	});



    $( "#confirm_button_k" ).click(function() {

        $.ajax({
        url: "/api/crawl/",
        method : "POST",
        type: "POST",
        data: {
            target: "korr"
        } ,
        success: function (resp) {
          if (resp.error) {
                alert("Error");
                return;
            }

            var state = {
                crawlingStatus: null,
                data: null,
                taskID: null,
                statusInterval: 1
            };

            state.taskID = resp.task_id;
            state.crawlingStatus = resp.status;
            state.statusInterval = setInterval(checkCrawlStatus, 2000, state);

        },
        error: function(jqXHR, textStatus, errorThrown) {
           console.log(textStatus, errorThrown);
        }
        });

	});

    function checkCrawlStatus(state){
        $.ajax({
        url: "/api/crawl/",
        data: {
            task_id: state.taskID
        } ,
        success: function (resp) {

          if (resp.data) {
                clearInterval(state.statusInterval);
                state.data = resp.data;
                alert(state.data);
            } else if (resp.error) {
                clearInterval(state.statusInterval);
                alert(resp.error);
            } else if (resp.status) {
                state.crawlingStatus = resp.status;
            } else {
                clearInterval(state.statusInterval);
            }

        },
        error: function(jqXHR, textStatus, errorThrown) {
           alert("ERROR");
           console.log(textStatus, errorThrown);
        }
        });
    }


});