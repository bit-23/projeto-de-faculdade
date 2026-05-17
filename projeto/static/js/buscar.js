document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // ELEMENTOS
    // =========================
    const cards = document.querySelectorAll(".job-card");

    const busca = document.getElementById("buscar");

    const categorias =
        document.querySelectorAll(".cat");

    const valores =
        document.querySelectorAll(".valor");

    const ordenar =
        document.getElementById("ordenar");

    const lista =
        document.getElementById("listaPropostas");

    // =========================
    // ESTADO
    // =========================
    let categoriaAtual = "todos";

    let min = 0;
    let max = 999999;

    // =========================
    // FILTRAR
    // =========================
    function atualizar() {

        cards.forEach(card => {

            const titulo =
                card.querySelector("h2")
                .textContent
                .toLowerCase();

            const descricao =
                card.querySelector("p")
                .textContent
                .toLowerCase();

            const categoria =
                card.dataset.cat;

            const valor =
                parseInt(card.dataset.valor);

            const texto =
                busca
                ? busca.value.toLowerCase()
                : "";

            const matchTexto =
                titulo.includes(texto)
                || descricao.includes(texto);

            const matchCategoria =
                categoriaAtual === "todos"
                || categoria === categoriaAtual;

            const matchValor =
                valor >= min
                && valor <= max;

            card.style.display =
                matchTexto
                && matchCategoria
                && matchValor
                ? "block"
                : "none";

        });

    }

    // =========================
    // BUSCA
    // =========================
    if (busca) {

        busca.addEventListener(
            "input",
            atualizar
        );

    }

    // =========================
    // CATEGORIAS
    // =========================
    categorias.forEach(btn => {

        btn.addEventListener("click", () => {

            categorias.forEach(b => {
                b.classList.remove("ativo");
            });

            btn.classList.add("ativo");

            categoriaAtual =
                btn.dataset.cat;

            atualizar();

        });

    });

    // =========================
    // FILTRO DE VALOR
    // =========================
    valores.forEach(btn => {

        btn.addEventListener("click", () => {

            min =
                parseInt(btn.dataset.min);

            max =
                parseInt(btn.dataset.max);

            atualizar();

        });

    });

    // =========================
    // ORDENAR
    // =========================
    if (ordenar && lista) {

        ordenar.addEventListener("change", () => {

            const array = [...cards];

            array.sort((a, b) => {

                const va =
                    parseInt(a.dataset.valor);

                const vb =
                    parseInt(b.dataset.valor);

                // maior valor
                if (ordenar.value === "maior") {

                    return vb - va;

                }

                // menor valor
                if (ordenar.value === "menor") {

                    return va - vb;

                }

                return 0;

            });

            array.forEach(card => {

                lista.appendChild(card);

            });

        });

    }

});