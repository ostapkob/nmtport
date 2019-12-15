    function progress_per_shift(data) {
      for (var key in data) {
        document.write('<div class="name-mech">'+ valByMins[key].name+ '  ' );
        document.write('<span class="badge badge-secondary">' + valByMins[key].total + '</span></div>');
        progress_bar_time(valByMins[key].data, shift); 
      }
    }

    function hours(shift){
      if (shift==1) {
        hs = ["║",  "╵", "09",  "╵", "10",  "╵", "11",  "╵", "12",  "╵", "13",  "╵", "14",  "╵", "15",  "╵", "16",  "╵", "17",  "╵", "18",  "╵", "19",  "╵",  "║"] }
        else {
          hs = ["║",  "╵", "21",  "╵", "22",  "╵", "23",  "╵", "00",  "╵", "01",  "╵", "02",  "╵", "03",  "╵", "04",  "╵", "05",  "╵", "06",  "╵", "07",  "╵",  "║"] }
          document.write(' <div class="d-flex justify-content-between line-mech">');
          for (var h in hs) {
            document.write('<div class="text-center time-mech">'+hs[h]+'</div>');
          }
          document.write(' </div> ');
        }

        
        function progress_bar_time(list, shift){
          document.write('<div class="progress">') ;
          for (var id in list) {
            n=list[id].value;
            if (n==-1){
              document.write('<div class="progress-bar bg-danger" role="progressbar"  style="width: 0.14%" ></div>'); }
              else if (n==0){
                document.write('<div class="progress-bar bg-warning"  role="progressbar" style="width: 0.14%"></div>'); }
                else {
                  document.write('<div class="progress-bar"  role="progressbar" style="width: 0.14%"></div>') ; }
                }
                document.write('</div>');
                hours(shift);
              }

  // function progress_bar_time_test(list, shift){
  //   document.write('<div class="progress">') ;
  //   var tmp = -1;
  //   var lengthBar=0;
  //   var start=0;
  //   var count=0;

  //   for (var id in list) {
  //       n=list[id].value;

  //       if (n!=tmp) {
  //          tmp=n;
  //          start=list[id].time;
  
  //           <!-- document.write(lengthBar+' | '); --> 
  //           if (n==-1){
  //               document.write('<div class="progress-bar bg-danger" role="progressbar"  style="width:'+ lengthBar+ '%" ></div>'); }
  //           else if (n==0){
  //               document.write('<div class="progress-bar bg-warning"  role="progressbar" style="width:'+lengthBar + '%"></div>'); }
  //           else {
  //               document.write('<div class="progress-bar"  role="progressbar" style="width:' + lengthBar +'%"></div>') ; }
  //           lengthBar=0;
  //           }
  //       else {
  //           count++;
  //           lengthBar+=0.139;
  //       }
  //   }
  //   document.write('</div>');
  //   hours(shift);
  //   tmp = -1;
  //   lengthBar=0;
  //   start=0;
  //   count=0;
  //   }
