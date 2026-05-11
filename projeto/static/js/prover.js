// static/js/prover.js

document.addEventListener("DOMContentLoaded", () => {

    const cards = document.querySelectorAll(".job-card");
    const busca = document.getElementById("buscar");
    const categorias = document.querySelectorAll(".cat");
    const valores = document.querySelectorAll(".valor");
    const ordenar = document.getElementById("ordenar");
    const modal = document.getElementById("modal");

    let categoriaAtual = "todos";
    let min = 0;
    let max = 999999;

    // =========================
    // FILTRAR
    // =========================
    function atualizar() {

        cards.forEach(card => {

            const titulo = card.querySelector("h2").textContent.toLowerCase();

            const cat = card.dataset.cat;

            const valor = parseInt(card.dataset.valor);

            const texto = busca
                ? busca.value.toLowerCase()
                : "";

            const matchTexto = titulo.includes(texto);

            const matchCat =
                categoriaAtual === "todos"
                || cat === categoriaAtual;

            const matchValor =
                valor >= min
                && valor <= max;

            card.style.display =
                matchTexto && matchCat && matchValor
                ? "block"
                : "none";

        });

    }

    // =========================
    // BUSCA
    // =========================
    if (busca) {

        busca.addEventListener("input", atualizar);

    }

    // =========================
    // CATEGORIAS
    // =========================
    categorias.forEach(btn => {

        btn.onclick = () => {

            categorias.forEach(b => {
                b.classList.remove("ativo");
            });

            btn.classList.add("ativo");

            categoriaAtual = btn.dataset.cat;

            atualizar();

        };

    });

    // =========================
    // VALORES
    // =========================
    valores.forEach(btn => {

        btn.onclick = () => {

            min = parseInt(btn.dataset.min);

            max = parseInt(btn.dataset.max);

            atualizar();

        };

    });

    // =========================
    // ORDENAR
    // =========================
    if (ordenar) {

        ordenar.onchange = () => {

            const lista =
                document.getElementById("listaPropostas");

            const array = [...cards];

            array.sort((a, b) => {

                let va = parseInt(a.dataset.valor);

                let vb = parseInt(b.dataset.valor);

                if (ordenar.value === "maior")
                    return vb - va;

                if (ordenar.value === "menor")
                    return va - vb;

                return 0;

            });

            array.forEach(card => {
                lista.appendChild(card);
            });

        };

    }

    // =========================
    // MODAL
    // =========================
    const abrir =
        document.getElementById("abrirModal");

    const fechar =
        document.getElementById("fecharModal");

    if (abrir && modal) {

        abrir.onclick = () => {

            modal.classList.remove("hidden");

        };

    }

    if (fechar && modal) {

        fechar.onclick = () => {

            modal.classList.add("hidden");

        };

    }

});