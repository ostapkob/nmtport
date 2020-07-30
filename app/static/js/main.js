    function progress_per_shift(data) {
        if (type_mechanism=='usm' ) {
        document.write('<em> <span class="badge badge-dark">   1.1</span> - время нахождения угля на ленте   ');
        document.write('<span class="badge badge-primary">1.2</span> - время работы    ');
        document.write('<span class="badge badge-info">   1.3</span> - время работы c учетом простоев </em>');
        }

      for (var key in data) {
        document.write('<div class="name-mech">'+ valByMins[key].name+ '  ' );

        if (type_mechanism=='usm' ) {
        document.write('<span class="badge badge-dark">' + valByMins[key].time_coal + '</span> ');
        document.write('<span class="badge badge-primary">' + valByMins[key].work_time + '</span> ');
        document.write('<span class="badge badge-info">' + valByMins[key].total_time + '</span> ');
        }

        if (type_mechanism=='kran' ) {
        document.write('<span class="badge badge-primary"> ' + valByMins[key].total_180 + '</span> ');
        document.write('<span class="badge badge-dark">' + valByMins[key].total_90 + '</span>');
        }
        document.write('<span class="time-start-finish text-right"> start <strong>' + valByMins[key].start + '</strong> </span>');
        document.write('<span class="time-start-finish text-right"> finish <strong>' + valByMins[key].finish + '</strong> </span></div>');
        progress_bar_time(valByMins[key].data, shift); 
      }
    }

    function hours(shift){
      if (shift==1) {
        // hs = ["║",  "╵", "09",  "╵", "10",  "╵", "11",  "╵", "12",  "╵", "13",  "╵", "14",  "╵", "15",  "╵", "16",  "╵", "17",  "╵", "18",  "╵", "19",  "╵",  "║"] }
        hs = ["║",  "╵","│","╵", "09",  "╵","│","╵", "10",  "╵", "│","╵","11",  "╵","│","╵", "12",  "╵","│","╵", "13",  "╵","│","╵", "14",  "╵","│","╵", "15",  "╵","│","╵", "16",  "╵","│","╵", "17",  "╵","│","╵", "18",  "╵","│","╵", "19",  "╵","│","╵",  "║"] }
        else {
          // hs = ["║",  "╵", "21",  "╵", "22",  "╵", "23",  "╵", "00",  "╵", "01",  "╵", "02",  "╵", "03",  "╵", "04",  "╵", "05",  "╵", "06",  "╵", "07",  "╵",  "║"] }
          hs = ["║",  "╵","│","╵", "21",  "╵","│","╵", "22",  "╵", "│","╵","23",  "╵","│","╵", "00",  "╵","│","╵", "01",  "╵","│","╵", "02",  "╵","│","╵", "03",  "╵","│","╵", "04",  "╵","│","╵", "05",  "╵","│","╵", "06",  "╵","│","╵", "07",  "╵","│","╵",  "║"] }
          document.write(' <div class="d-flex justify-content-between line-mech">');
          for (var h in hs) {
            document.write('<div class="text-center time-mech">'+hs[h]+'</div>');
          }
          document.write(' </div> ');
        }

        
        function progress_bar_time(list, shift){
            console.log(type_mechanism);
            document.write('<div class="progress">') ;

        if (type_mechanism=='usm' ) {
          for (var id in list) {
            n=list[id].value;
            width = list[id].step*0.139; 
            if (n==-1){
              document.write('<div class="progress-bar progress-bar-striped bg-danger time-progress text-left" role="progressbar"  style="width:' + width + '%" >' + list[id].time + '</div>'); }
              else if (n==0){
                document.write('<div class="progress-bar bg-warning text-left time-progress text-dark"  role="progressbar" style="width:' + width +'%">' + list[id].time + '</div>'); }
                else {
                  document.write('<div class="progress-bar time-progress text-left"  role="progressbar" style="width:' + width + '%">' + list[id].time + '</div>') ; }
                }
        }


        if (type_mechanism=='kran' ) {
          for (var id in list) {
            n=list[id].value;
            if (n==-1){
              document.write('<div class="progress-bar progress-bar-striped bg-danger" role="progressbar"  style="width: 0.14%" ></div>'); }
              else if (n==0){
                document.write('<div class="progress-bar bg-warning"  role="progressbar" style="width: 0.14%"></div>'); }
              else if (n==1){
                document.write('<div class="progress-bar bg-dark"  role="progressbar" style="width: 0.14%"></div>'); }
                else {
                  document.write('<div class="progress-bar"  role="progressbar" style="width: 0.14%"></div>') ; }
                }
        }






                document.write('</div>');
                hours(shift);
              }
