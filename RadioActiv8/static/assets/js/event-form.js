function dynamic_form_update(){
  var patrol = jQuery("#id_patrol").val();
  var location = jQuery("#id_location").val();

  //var url = "{% url 'RadioActiv8:event_ajax' %}"
  var url = jQuery('#id_patrol').closest('form').attr('data-ajax-url')
  jQuery.ajax({
    url: url,
    data: {
      'patrol': patrol,
      'current_location': location
    },
    success: function (data) {

      { // Update Intelligence drop-down
        var intelligence = "<option value=''>---------</option>";

        intelligence += "<option value=''>--- Available intelligence</option>";
        // Unused intelligence
        var random_intelligence = Math.floor(Math.random() * data.intelligence_options.unused.length);
        for (var i = 0; i < data.intelligence_options.unused.length; i++) {
          var int = data.intelligence_options.unused[i];
          var selected = (i == random_intelligence) ? ' selected=""' : '';

          intelligence += "<option value='" + int.id + "'" + selected + ">" + int.q + " - " + int.a + "</option>";
        }
        intelligence += "<option value=''>--- Used intelligence</option>";
        // Used intelligence
        for (var i = 0; i < data.intelligence_options.used.length; i++) {
          var int = data.intelligence_options.used[i];
          intelligence += "<option value='" + int.id + "'>" + int.q + " - " + int.a + "</option>";
        }
        jQuery("#id_intelligence_request").html(intelligence);

      }

      { // Update Destination drop-down
        var destination = "<option value=''>---------</option>";

        destination += "<option value=''>--- Unvisited Bases</option>";

        // Unvisited bases
        var random_base = Math.floor(Math.random() * data.valid_destinations.unvisited.length);
        for (var i = 0; i < data.valid_destinations.unvisited.length; i++) {
          var base = data.valid_destinations.unvisited[i];
          var selected = (i == random_base) ? ' selected=""' : '';

          destination += "<option value='" + base.id + "'" + selected + ">" + base.b + "</option>";
        }
        destination += "<option value=''>--- Visited Bases</option>";
        // Visited bases
        for (var i = 0; i < data.valid_destinations.visited.length; i++) {
          var base = data.valid_destinations.visited[i];
          destination += "<option value='" + base.id + "'>" + base.b + "</option>";
        }
        jQuery("#id_destination").html(destination);
      }

      { // Display Base history and last expected destination

        var base_history = '';
        for (var i = 0; i < data.base_history.visited_bases.length; i++) {
          var id = data.base_history.visited_bases[i].id
          var name = data.base_history.visited_bases[i].name
          base_history += "<li data.base_history-base-id='" + id + "'>" + name + "</li>"
        }
        jQuery("#base_history").html(base_history);

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
          jQuery("#expected_location").append("<strong> <--- ### WARNING! LOCATION MISMATCH! ###</strong>");
        }
      }
    }
  });

}

jQuery(document).ready(function(){
    jQuery("#id_intelligence_request").html('<option value="" selected="">---------</option>');
    jQuery("#id_destination").html('<option value="" selected="">---------</option>');
    dynamic_form_update();
    jQuery("#id_patrol").change(dynamic_form_update);
    jQuery("#id_location").change(dynamic_form_update);
})