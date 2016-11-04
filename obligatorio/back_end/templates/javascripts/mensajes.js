<script type="text/javascript">
  $(document).ready(function(){
    {%if not rows and buscar%}
      toastr.info('No se encontraron resultados para la busqueda "{{buscar}}"','info');
    {%endif%}
    {%if messages%}
      {%for message in messages%}
        {#tags viene de la vista#}
        {%comment%}
        o
        varias lines
        {%endcomment%}
        toastr.{{message.tags}}("{{message}}")
      {%endfor%}
    {%endif%}
  });
</script>
