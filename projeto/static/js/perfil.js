document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // FOTO
    // =========================
    const inputFoto =
        document.getElementById("inputFoto");

    const previewFoto =
        document.getElementById("previewFoto");

    if (inputFoto && previewFoto) {

        inputFoto.addEventListener("change", (event) => {

            const arquivo = event.target.files[0];

            if (arquivo) {

                const reader = new FileReader();

                reader.onload = (e) => {

                    previewFoto.src = e.target.result;

                    // salva temporariamente
                    localStorage.setItem(
                        "fotoPerfil",
                        e.target.result
                    );

                };

                reader.readAsDataURL(arquivo);

            }

        });

        // carregar foto salva
        const fotoSalva =
            localStorage.getItem("fotoPerfil");

        if (fotoSalva) {

            previewFoto.src = fotoSalva;

        }

    }

    // =========================
    // EDITAR PERFIL
    // =========================
    const botaoEditar =
        document.querySelector(".btn-editar");

    const inputs =
        document.querySelectorAll(".campo input");

    let editando = false;

    if (botaoEditar) {

        botaoEditar.addEventListener("click", () => {

            editando = !editando;

            inputs.forEach(input => {

                input.disabled = !editando;

            });

            botaoEditar.textContent =
                editando
                ? "Salvar Alterações"
                : "Editar Perfil";

        });

    }

});