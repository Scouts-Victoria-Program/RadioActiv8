function destination_toggle() {
  if (jQuery("#radio-check-in:checked").val() == "on") {
    jQuery("#destination_form_group").hide();
    var location_field = jQuery("#id_location");
    var destination_field = jQuery("#id_destination");
    destination_field.val(location_field.val());
  } else {
    jQuery("#destination_form_group").show();
    dynamic_form_update((destionation_toggle = true));
  }
}

function dynamic_form_update(destination_toggle = false) {
  var current_session = jQuery("#id_session").val();
  var current_patrol = jQuery("#id_patrol").val();
  var current_location = jQuery("#id_location").val();

  //var url = "{% url 'RadioActiv8:event_ajax' %}"
  var url = jQuery('#id_patrol').closest('form').attr('data-ajax-url')
  // FIXME: This is a hack to work with the <form> element created by Django Admin
  if (!url) { url = jQuery('#ajax_form_url').attr('data-ajax-url'); }
  jQuery.ajax({
    url: url,
    data: {
      'ra8_session': current_session,
      'patrol': current_patrol,
      'current_location': current_location
    },
    success: function (data) {

      { // Update Patrol drop-down
        var patrol = "<option value=''>---------</option>";
        for(var i = 0; i < data.patrol_options.length; i++) {
          var p = data.patrol_options[i];
          var selected = (p.id == current_patrol) ? ' selected=""' : '';
          patrol += "<option value='" + p.id + "'" + selected + ">" + p.name + " (" + p.number_of_members + " members) </option>";
        }
        jQuery("#id_patrol").html(patrol);
      }

      { // Update Location drop-down
        var location = "<option value=''>---------</option>";
        var current_session_locations = ""
        var non_session_locations = ""
        for(var i = 0; i < data.location_options.length; i++) {
          var loc = data.location_options[i];
          var selected = (loc.id == current_location) ? ' selected=""' : '';
          var this_location = "<option value='" + loc.id + "'" + selected + ">" + loc.name + "</option>";
          if(loc.current_session)
            current_session_locations += this_location;
          else non_session_locations += this_location;
        }
        location += "<optgroup label='Current Session'>";
        location += current_session_locations;
        location += "</optgroup>";
        location += "<optgroup label='Not in Session'>";
        location += non_session_locations;
        location += "</optgroup>";
        jQuery("#id_location").html(location);
      }

      {
        // Update Intelligence drop-down
        if (
          (data.intelligence_options.unused.length == 0 &&
            data.intelligence_options.used.length == 0) ||
          (data.intelligence_options.unused.length == undefined &&
            data.intelligence_options.used.length == undefined)
        ) {
          jQuery(".form-intelligence-request").hide();
        } else {
          jQuery(".form-intelligence-request").show();
        }

        var intelligence = "<option value=''>---------</option>";
        var selected_intelligence = jQuery("#id_intelligence_request").val()

        intelligence += "<optgroup label='Available intelligence'>";
        // Unused intelligence
        var random_intelligence = 0;
        if(data.intelligence_options.random)
          random_intelligence = Math.floor(Math.random() * data.intelligence_options.unused.length);
        else
          random_intelligence = -1;
        for (var i = 0; i < data.intelligence_options.unused.length; i++) {
          var int = data.intelligence_options.unused[i];
          if(selected_intelligence)
          {
            if(int.id == selected_intelligence)
            {
              var selected = ' selected=""';
              jQuery('#intelligence_suggestion').html("Q: " + int.q + "? <br>A: " + int.a )
            }
            else var selected = '';
          }
          else var selected = (i == random_intelligence) ? ' selected=""' : '';
          if(int.q.length > 20) question = int.q.substring(0,20) + '…';
          else question = int.q;
          if(int.a.length > 20) answer = int.a.substring(0,20) + '…';
          else answer = int.a;
          intelligence += "<option value='" + int.id + "'" + selected + "> Q: " + question + "? A: " + answer + "</option>";
        }
        intelligence += "</optgroup>";
        intelligence += "<optgroup label='Used intelligence'>";
        // Used intelligence
        for (var i = 0; i < data.intelligence_options.used.length; i++) {
          var int = data.intelligence_options.used[i];
          if(int.q.length > 20) question = int.q.substring(0,20) + '…';
          else question = int.q;
          if(int.a.length > 20) answer = int.a.substring(0,20) + '…';
          else answer = int.a;
          intelligence += "<option value='" + int.id + "'> Q: " + question + "? A: " + answer + "</option>";
        }
        intelligence += "</optgroup>";
        jQuery("#id_intelligence_request").html(intelligence);

      }

      { // Update Destination drop-down
        var destination = "<option value=''>---------</option>";
        var visited = [];
        var full = [];
        var facilitated = [];
        var unvisited = [];
        var base_choice = []
        if (!data.valid_destinations.bases) return;
        for (var i = 0; i < data.valid_destinations.bases.length; i++)
        {
          var base = data.valid_destinations.bases[i];
          if (base.time != null) {
            min = Math.floor(base.time / 60)
            sec = base.time % 60
            /*min = String(min).padStart(2, '0')
            sec = String(sec).padStart(2, '0')
            base.name = `${base.name} (${min}:${sec})`;*/
            base.name = `${base.name} (${min}m ${sec}s)`;
          }
          if (base.visited) {
            visited.push(base);
          }
          else if(base.max_patrols != null && base.num_patrols >= base.max_patrols)
          {
            full.push(base);
          }
          else if(base.type == 'F')
          {
            facilitated.push(base);
            for(var j = 0; j < (base.max_patrols - base.num_patrols); j++)
            {
              base_choice.push(base.id);
            }
          }
          else
          {
            unvisited.push(base);
          }
        }

        var suggested_base = null;
        if(facilitated.length)
        {
          var random_base = Math.floor(Math.random() * base_choice.length);
          suggested_base = base_choice[random_base];
        } else if(unvisited.length)
        {
          var random_base = Math.floor(Math.random() * unvisited.length);
          suggested_base = unvisited[random_base].id;
        }

        // Facilitated bases
        destination += "<optgroup label='Available Facilitated Bases'>";
        for (var i = 0; i < facilitated.length; i++)
        {
          base = facilitated[i];
          var selected = (base.id == suggested_base) ? ' selected=""' : '';
          destination += "<option value='" + base.id + "'" + selected + ">" + base.name + "</option>";
        }
        destination += "</optgroup>";
        // Unvisited bases
        destination += "<optgroup label='Unvisited Non-facilitated Bases'>";
        for (var i = 0; i < unvisited.length; i++)
        {
          base = unvisited[i];
          var selected = (base.id == suggested_base) ? ' selected=""' : '';
          destination += "<option value='" + base.id + "'" + selected + ">" + base.name + "</option>";
        }
        destination += "</optgroup>";
        // Full bases
        destination += "<optgroup label='Full Facilitated Bases'>";
        for (var i = 0; i < full.length; i++)
        {
          base = full[i];
          var selected = (base.id == suggested_base) ? ' selected=""' : '';
          destination += "<option value='" + base.id + "'" + selected + ">" + base.name + "</option>";
        }
        destination += "</optgroup>";
        // Visited bases
        destination += "<optgroup label='Visited Bases'>";
        for (var i = 0; i < visited.length; i++)
        {
          base = visited[i];
          var selected = (base.id == suggested_base) ? ' selected=""' : '';
          var repeatable = (base.repeatable) ? '' : " (NOT REPEATABLE!)";
          destination += "<option value='" + base.id + "'" + selected + ">" + base.name + repeatable + "</option>";
        }
        destination += "</optgroup>";


        if(data.valid_destinations.home_base)
        {
          var home_base = data.valid_destinations.home_base;
          destination += "<optgroup label='Home Base'>";
          destination += "<option value='" + home_base.id +  "'>" + home_base.name + "</option>";
          destination += "</optgroup>";
        }
        jQuery("#id_destination").html(destination);
        if (!destination_toggle) {
          if (data.check_in) {
            jQuery("#radio-check-in").prop("checked", "checked");
            jQuery("#destination_form_group").hide();
            var location_field = jQuery("#id_location");
            var destination_field = jQuery("#id_destination");
            destination_field.val(location_field.val());
          } else {
            jQuery("#radio-check-out").prop("checked", "checked");
            jQuery("#destination_form_group").show();
          }
        }
      }

      { // Display Base history, commentary and last expected destination

        var base_history = '';
        for (var i = 0; i < data.base_history.visited_bases.length; i++) {
          var id = data.base_history.visited_bases[i].id
          var name = data.base_history.visited_bases[i].name
          base_history += "<li data.base_history-base-id='" + id + "'>" + name + "</li>"
        }
        jQuery("#base_history").html(base_history);

        var comment_history = '';
        for (var i = 0; i < data.comment_history.length; i++) {
          var timestamp = data.comment_history[i].timestamp
          var comment = data.comment_history[i].comment
          comment_history += "<li><em>" + timestamp + "</em><br/>" + comment + "</li>"
        }
        jQuery("#comment_history").html(comment_history);

        var expected_location = data.base_history.last_destination;
        if(!expected_location)
        {
          expected_location = Object();
          expected_location.id = -1;
          expected_location.name = "UNKNOWN"
        }
        jQuery("#expected_location").html(expected_location.name);
        jQuery("#expected_location").attr('data-location-id', expected_location.id);

        var actual_location_id = jQuery('#id_location').val();

        // If we know an expected location but don't yet have a current location
        // set yet, set the current location to the expected one.
        if (expected_location.id && expected_location.id != -1 &&
          actual_location_id === "") {
          actual_location_id = expected_location.id;
          jQuery('#id_location').val(actual_location_id);
          // FIXME: Recursive function call; this could be nasty...
          dynamic_form_update();
        }

        // If we have a valid expected location and a valid current location,
        // and they don't match, warn the user
        if (expected_location.id != -1 &&
          !(actual_location_id === "") &&
          expected_location.id != actual_location_id) {
          jQuery("#expected_location").append("<strong>&nbsp;### WARNING! LOCATION MISMATCH! ###</strong>");
          jQuery("#expected_location").removeClass('alert-info');
          jQuery("#expected_location").addClass('alert-danger');
        }
        else
        {
          jQuery("#expected_location").addClass('alert-info');
          jQuery("#expected_location").removeClass('alert-danger');
        }
      }
    }
  });

}
jQuery(document).ready(function () {
  jQuery(".form-intelligence-request").hide();
  if (!jQuery && django.jQuery) {
    jQuery = django.jQuery;
  }
  jQuery("#id_intelligence_request").html(
    '<option value="" selected="">---------</option>'
  );
  jQuery("#id_destination").html(
    '<option value="" selected="">---------</option>'
  );
  destination_toggle();
  dynamic_form_update();
  jQuery("#id_session").change(dynamic_form_update);
  jQuery("#id_patrol").change(function () {
    jQuery("#id_location").val(0);
  });
  jQuery("#id_patrol").change(dynamic_form_update);
  jQuery("#id_location").change(dynamic_form_update);
  jQuery("#id_intelligence_request").change(dynamic_form_update);

  jQuery("#radio-check-in").change(destination_toggle);
  jQuery("#radio-check-out").change(destination_toggle);
});
