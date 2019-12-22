
function initMap() {
      var mapOptions = {
        center: {lat: 42.8120, lng: 132.8900},
        zoom: 16,

        mapTypeId: google.maps.MapTypeId.SATELLITE
      };
      var map = new google.maps.Map(document.getElementById('map'),mapOptions);

      var info = new google.maps.InfoWindow({
        content: '<h4> 7.5 </h4> <p> Demendge </p>'
      })

      var S5  = new google.maps.Marker({
        position: {lat: 42.8155, lng: 132.8910},
        title: 'Screen5',
        draggable: true,
        animation: google.maps.Animation.DROP,
        icon: 'http://maps.google.com/mapfiles/kml/pal3/icon12.png',
        map: map
      });

      // var S6  = new google.maps.Marker({
      //   position: {lat: 42.8120, lng: 132.8888},
      //   title: 'Screen6',
      //   animation: google.maps.Animation.DROP,
      //   icon: 'http://maps.google.com/mapfiles/kml/pal3/icon13.png',
      //   map: map
      // });
      var S7  = new google.maps.Marker({
        position: {lat: 42.8082, lng: 132.8862},
        animation: google.maps.Animation.DROP,
        icon: 'http://maps.google.com/mapfiles/kml/pal3/icon14.png',
        title: 'Screen7',
        map: map
      });
      var S6  = new google.maps.Marker({
        position: {lat: 42.8210, lng: 132.8800},
        title: 'Screen6',
        animation: google.maps.Animation.DROP,
        icon: 'http://maps.google.com/mapfiles/kml/pal3/icon13.png',
        map: map
      });
        // marker.addListener("mouseover", function() {info.open(map, marker);
          S5.addListener("mouseover", function() {info.open(map, S5);  });
          S5.addListener("mouseout", function() {info.close(map, S5);  });
    }



