<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>

<script>
      $(document).ready(function() {
        $('#clientName').change(function() {

          var cl = $('#clientName').val();

          // Make Ajax Request and expect JSON-encoded data
          $.getJSON(
            '/get_food' + '/' + cl,
            function(data) {

              // Remove old options
              $('#Legal').find('option').remove();                                

              // Add new items
              $.each(data, function(key, val) {
                var option_item = '<option value="' + val + '">' + val + '</option>'
                $('#Legal').append(option_item);
              });
            }
          );
        });
      });
    </script>
