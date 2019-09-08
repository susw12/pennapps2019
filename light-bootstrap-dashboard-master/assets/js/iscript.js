$(function(){
    new jvm.MultiMap({
      container: $('#map'),
      maxLevel: 1,
      main: {
        map: 'us_lcc'
      },
      mapUrlByCode: function(code, multiMap){
        return '/js/us-counties/jquery-jvectormap-data-'+
               code.toLowerCase()+'-'+
               multiMap.defaultProjection+'-en.js';
      }
    });
  });

  $('#map').vectorMap({map: 'us_aea'});
