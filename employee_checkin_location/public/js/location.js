//for fetch the currect location in employee checkin doctype 
frappe.ui.form.on('Employee Checkin', {
	onload(frm) {
	    // onload of employee checkin doctype
	    function onPositionRecieved(position){
	        var longitude= position.coords.longitude;
	        var latitude= position.coords.latitude;
	        frm.set_value('longitude',longitude);
	        frm.set_value('latitude',latitude);
	        console.log(longitude);
	        console.log(latitude);
	        // getting current loaction data using api
	        fetch('https://api.opencagedata.com/geocode/v1/json?q='+latitude+'+'+longitude+'&key=de1bf3be66b546b89645e500ec3a3a28')
	         .then(response => response.json())
            .then(data => {
                var city=data['results'][0].components.city;
                var state=data['results'][0].components.state;
                var area=data['results'][0].components.residential;
                frm.set_value('city',city);
                frm.set_value('state',state);
                frm.set_value('area',area);
                console.log(data);
            })
            .catch(err => console.log(err));
	        frm.set_df_property('my_location','options','<div class="mapouter"><div class="gmap_canvas"><iframe width=100% height="300" id="gmap_canvas" src="https://maps.google.com/maps?q='+latitude+','+longitude+'&t=&z=17&ie=UTF8&iwloc=&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe><a href="https://yt2.org/youtube-to-mp3-ALeKk00qEW0sxByTDSpzaRvl8WxdMAeMytQ1611842368056QMMlSYKLwAsWUsAfLipqwCA2ahUKEwiikKDe5L7uAhVFCuwKHUuFBoYQ8tMDegUAQCSAQCYAQCqAQdnd3Mtd2l6"></a><br><style>.mapouter{position:relative;text-align:right;height:300px;width:100%;}</style><style>.gmap_canvas {overflow:hidden;background:none!important;height:300px;width:100%;}</style></div></div>');
            frm.refresh_field('my_location');
	    }
	    
	    function locationNotRecieved(positionError){
	        console.log(positionError);
	    }

	    if(frm.doc.longitude && frm.doc.latitude){
	        frm.set_df_property('my_location','options','<div class="mapouter"><div class="gmap_canvas"><iframe width=100% height="300" id="gmap_canvas" src="https://maps.google.com/maps?q='+frm.doc.latitude+','+frm.doc.longitude+'&t=&z=17&ie=UTF8&iwloc=&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe><a href="https://yt2.org/youtube-to-mp3-ALeKk00qEW0sxByTDSpzaRvl8WxdMAeMytQ1611842368056QMMlSYKLwAsWUsAfLipqwCA2ahUKEwiikKDe5L7uAhVFCuwKHUuFBoYQ8tMDegUAQCSAQCYAQCqAQdnd3Mtd2l6"></a><br><style>.mapouter{position:relative;text-align:right;height:300px;width:100%;}</style><style>.gmap_canvas {overflow:hidden;background:none!important;height:300px;width:100%;}</style></div></div>');
            frm.refresh_field('my_location');
	    } else {
	        if(navigator.geolocation){
	            navigator.geolocation.getCurrentPosition(onPositionRecieved,locationNotRecieved,{ enableHighAccuracy: true});
	        }
	    }
    }
})