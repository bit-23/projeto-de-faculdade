document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // FOTO - apenas preview local
    // =========================
    const inputFoto = document.getElementById("inputFoto");
    const previewFoto = document.getElementById("previewFoto");

    if (inputFoto && previewFoto) {
        inputFoto.addEventListener("change", (event) => {
            const arquivo = event.target.files[0];
            if (arquivo) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    previewFoto.src = e.target.result;
                };
                reader.readAsDataURL(arquivo);
            }
        });
    }

    // =========================
    // EDITAR PERFIL
    // =========================
    const botaoEditar = document.querySelector(".btn-editar");
    const inputs = document.querySelectorAll(".campo input");
    let editando = false;

    if (botaoEditar) {
        botaoEditar.addEventListener("click", () => {
            editando = !editando;
            inputs.forEach(input => {
                input.disabled = !editando;
            });
            botaoEditar.textContent = editando ? "Salvar Alterações" : "Editar Perfil";
        });
    }

});