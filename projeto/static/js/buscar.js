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

// =========================
// MODAL DETALHES
// =========================
document.addEventListener("click", (e) => {
    if (e.target.classList.contains("btn-detalhes")) {

        const btn = e.target;

        const titulo      = btn.dataset.titulo;
        const descricao   = btn.dataset.descricao;
        const nomeCliente = btn.dataset.cliente;
        const fotoCliente = btn.dataset.fotoCliente;
        const categoria   = btn.dataset.categoria;
        const valorMin    = btn.dataset.valorMin;
        const valorMax    = btn.dataset.valorMax;
        const prazo       = btn.dataset.prazo;
        const fotoServico = btn.dataset.foto;
        const servicoId   = btn.dataset.id;

        // foto do serviço
        const divFoto = document.getElementById('modalFotoServico');
        if (fotoServico) {
            divFoto.innerHTML = `<img src="/static/uploads/${fotoServico}" style="width:100%;height:200px;object-fit:cover;border-radius:8px;margin-bottom:12px;">`;
        } else {
            divFoto.innerHTML = '';
        }

        // avatar do cliente
        const divAvatar = document.getElementById('modalAvatarCliente');
        if (fotoCliente) {
            divAvatar.innerHTML = `<img src="/static/uploads/${fotoCliente}" class="card-avatar" alt="${nomeCliente}">`;
        } else {
            divAvatar.innerHTML = `<div class="card-avatar-fallback">${nomeCliente[0].toUpperCase()}</div>`;
        }

        document.getElementById('modalNomeCliente').textContent = nomeCliente;
        document.getElementById('modalTitulo').textContent      = titulo;
        document.getElementById('modalDescricao').textContent   = descricao;
        document.getElementById('modalCategoria').textContent   = categoria;

        if (valorMin && valorMax) {
            document.getElementById('modalValor').textContent = `R$ ${valorMin} - R$ ${valorMax}`;
        } else if (valorMin) {
            document.getElementById('modalValor').textContent = `A partir de R$ ${valorMin}`;
        } else {
            document.getElementById('modalValor').textContent = 'A combinar';
        }

        document.getElementById('modalPrazo').textContent = prazo ? `${prazo} dias` : 'A definir';
        document.getElementById('formProposta').action = `/enviar_proposta/${servicoId}`;
        document.getElementById('modalDetalhes').classList.remove('hidden');
    }
});

document.getElementById('fecharDetalhes').onclick = () => {
    document.getElementById('modalDetalhes').classList.add('hidden');
};

document.getElementById('modalDetalhes').onclick = (e) => {
    if (e.target === document.getElementById('modalDetalhes')) {
        document.getElementById('modalDetalhes').classList.add('hidden');
    }
};