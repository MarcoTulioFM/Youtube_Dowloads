$(document).ready(function () {
    $('#sendButton').click(function () {
        var fileInput = $('#fileInput')[0].files[0];
        var formData = new FormData();
        formData.append('file', fileInput);

        var reader = new FileReader();
        reader.onload = function (e) {
            var fileContent = e.target.result;
            var links = fileContent.split('\n').filter(Boolean); // Separa o conteúdo do arquivo por quebras de linha
            var jsonData = {
                "type": "M",
                "links": links
            };

            $.ajax({
                url: 'http://34.29.180.186:9000/download',
                type: 'POST',
                data: JSON.stringify(jsonData),
                processData: false,
                contentType: 'application/json',
                success: function (response) {
                    alert('Arquivo enviado com sucesso!');
                },
                error: function () {
                    alert('Erro ao enviar arquivo.');
                }
            });
        };
        reader.readAsText(fileInput);
    });
});
