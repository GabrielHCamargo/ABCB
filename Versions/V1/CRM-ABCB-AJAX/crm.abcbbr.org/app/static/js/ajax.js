function consultaAutocomplete() {
    var nome_ou_cpf = $('#input-nome-ou-cpf').val();
    if (nome_ou_cpf.length >= 3) {
        $.ajax({
            url: '/autocomplete-cliente',
            method: 'POST',
            data: {'nome_ou_cpf': nome_ou_cpf},
            success: function(response) {
                var options = '';
                for (var i = 0; i < response.nomes.length; i++) {
                    options += '<option value="' + response.nomes[i] + '">';
                }
                $('#datalist-nomes').html(options);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert('Erro ao buscar nomes semelhantes.');
            }
        });
    }
}

function consultaCliente() {
    var nome_ou_cpf = $('#input-nome-ou-cpf').val();
    $('#ajax-content').html('<div class="loader"></div>');
    $.ajax({
        url: '/consulta-cliente',
        method: 'POST',
        data: {'nome_ou_cpf': nome_ou_cpf},
        success: function(response) {
            $('#ajax-content').html(response.html);
            $('.loader').hide();            
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert('Cliente não encontrado.');
            $('.loader').hide();
        }
    });
}

$(document).ready(function() {
    $('#input-nome-ou-cpf').on('keyup', function() {
        consultaAutocomplete();
    });
});

