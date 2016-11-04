<script type="text/javascript">
  <!--cuando termina de cargar DOM (Document Object model) ejecuta .ready-->
  $(document).ready(function(){
    {%if error%}
      toastr.error('{{error}}','Error');
    {%endif%}
    {%if success%}
    toastr.success('{{success}}','Datos correctos');
  {%endif%}
  });
</script>
