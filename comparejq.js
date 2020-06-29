<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>


<script>
      $(document).ready(function() {
        $('#client1').change(function() {

          var cl = $('#client1').val();

          // Make Ajax Request and expect JSON-encoded data
          $.getJSON(
            '/get_food' + '/' + cl,
            function(data) {

              // Remove old options
              $('#Legal1').find('option').remove();                                

              // Add new items
              $.each(data, function(key, val) {
                var option_item = '<option value="' + val + '">' + val + '</option>'
                $('#Legal1').append(option_item);
              });
            });
        });
      });


     $(document).ready(function() {
        $('#client2').change(function() {

          var cl = $('#client2').val();

          // Make Ajax Request and expect JSON-encoded data
          $.getJSON(
            '/get_food' + '/' + cl,
            function(data) {

              // Remove old options
              $('#Legal2').find('option').remove();                                

              // Add new items
              $.each(data, function(key, val) {
                var option_item = '<option value="' + val + '">' + val + '</option>'
                $('#Legal2').append(option_item);
              });
            });
        });
      });

    </script>