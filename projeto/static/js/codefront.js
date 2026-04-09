// ===== MÁSCARA DE CPF =====
function mascaraCPF(input) {
    let v = input.value.replace(/\D/g, '');
    v = v.replace(/(\d{3})(\d)/, '$1.$2');
    v = v.replace(/(\d{3})(\d)/, '$1.$2');
    v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    input.value = v;
}

// ===== VALIDADOR DE EMAIL =====
function emailValido(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// ===== VALIDADOR DE CPF =====
function cpfValido(cpf) {
    cpf = cpf.replace(/\D/g, '');
    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;

    let soma = 0;
    for (let i = 0; i < 9; i++) soma += parseInt(cpf.charAt(i)) * (10 - i);
    let resto = (soma * 10) % 11;
    if (resto === 10) resto = 0;
    if (resto !== parseInt(cpf.charAt(9))) return false;

    soma = 0;
    for (let i = 0; i < 10; i++) soma += parseInt(cpf.charAt(i)) * (11 - i);
    resto = (soma * 10) % 11;
    if (resto === 10) resto = 0;
    return resto === parseInt(cpf.charAt(10));
}

// ===== FORÇA DA SENHA =====
function forcaSenha(senha) {
    let forca = 0;
    if (senha.length >= 6) forca++;
    if (senha.length >= 10) forca++;
    if (/[A-Z]/.test(senha)) forca++;
    if (/[0-9]/.test(senha)) forca++;
    if (/[^A-Za-z0-9]/.test(senha)) forca++;
    return forca; // 0-5
}

// ===== ESTADO DE VALIDAÇÃO =====
function setEstado(input, valido) {
    input.classList.remove('valido', 'invalido');
    input.classList.add(valido ? 'valido' : 'invalido');
}

// ===== TOGGLE MOSTRAR/OCULTAR SENHA =====
function initToggleSenha(idInput, idBtn) {
    const input = document.getElementById(idInput);
    const btn = document.getElementById(idBtn);
    if (!input || !btn) return;

    btn.addEventListener('click', () => {
        const isPassword = input.type === 'password';
        input.type = isPassword ? 'text' : 'password';
        btn.setAttribute('stroke', isPassword ? '#4a6cf7' : '#888');
    });
}

// ===== LÓGICA DE CADASTRO =====
function initCadastro() {
    const form = document.querySelector('.login-box form');
    if (!form) return;

    if (!form.getAttribute('action')?.includes('cadastro') &&
        !document.querySelector('.login-box h2')?.textContent.includes('Criar')) return;

    const nomeInput = form.querySelector('input[name="nome"]');
    const emailInput = form.querySelector('input[name="email"]');
    const cpfInput = form.querySelector('input[name="CPF"]');
    const senhaInput = form.querySelector('input[name="senha"]');

    // --- Máscara de CPF ---
    if (cpfInput) {
        cpfInput.addEventListener('input', () => mascaraCPF(cpfInput));
    }

    // --- Barra de força da senha ---
    if (senhaInput) {
        const barraContainer = document.createElement('div');
        barraContainer.className = 'forca-container';
        barraContainer.innerHTML = `
            <div class="forca-bar"><div class="forca-fill"></div></div>
            <span class="forca-text"></span>
        `;
        senhaInput.parentElement.insertBefore(barraContainer, senhaInput.nextSibling);

        const forcaFill = barraContainer.querySelector('.forca-fill');
        const forcaText = barraContainer.querySelector('.forca-text');

        const niveis = ['', 'Muito fraca', 'Fraca', 'Razoável', 'Forte', 'Muito forte'];
        const cores = ['', '#e03131', '#f76707', '#fcc419', '#51cf66', '#2b8a3e'];

        senhaInput.addEventListener('input', () => {
            const nivel = forcaSenha(senhaInput.value);
            forcaFill.style.width = (nivel / 5 * 100) + '%';
            forcaFill.style.background = cores[nivel];
            forcaText.textContent = senhaInput.value ? niveis[nivel] : '';
        });
    }

    // --- Validação no submit ---
    form.addEventListener('submit', (e) => {
        let valido = true;

        if (nomeInput && nomeInput.value.trim().length < 3) {
            setEstado(nomeInput, false); valido = false;
        } else if (nomeInput) {
            setEstado(nomeInput, true);
        }

        if (emailInput && !emailValido(emailInput.value)) {
            setEstado(emailInput, false); valido = false;
        } else if (emailInput) {
            setEstado(emailInput, true);
        }

        if (cpfInput && !cpfValido(cpfInput.value)) {
            setEstado(cpfInput, false); valido = false;
        } else if (cpfInput) {
            setEstado(cpfInput, true);
        }

        if (senhaInput && senhaInput.value.length < 6) {
            setEstado(senhaInput, false); valido = false;
        } else if (senhaInput) {
            setEstado(senhaInput, true);
        }

        if (!valido) e.preventDefault();
    });

    // --- Validação on blur ---
    [nomeInput, emailInput, cpfInput, senhaInput].forEach(input => {
        if (!input) return;
        input.addEventListener('blur', () => {
            if (!input.value) {
                input.classList.remove('valido', 'invalido');
                return;
            }
            if (input === emailInput) setEstado(input, emailValido(input.value));
            else if (input === cpfInput) setEstado(input, cpfValido(input.value));
            else setEstado(input, input.value.trim().length >= (input === senhaInput ? 6 : 3));
        });
    });
}

// ===== LÓGICA DE LOGIN =====
function initLogin() {
    const form = document.querySelector('.login-box form');
    if (!form) return;

    const titulo = document.querySelector('.login-box h2');
    if (!titulo?.textContent.includes('Login')) return;

    const emailInput = form.querySelector('input[type="email"]');

    form.addEventListener('submit', (e) => {
        if (emailInput && !emailValido(emailInput.value)) {
            e.preventDefault();
        }
    });
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
    initToggleSenha('senha-cadastro', 'toggle-senha-cadastro');
    initToggleSenha('senha-login', 'toggle-senha-login');
    initCadastro();
    initLogin();
});
