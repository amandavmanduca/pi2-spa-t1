new Vue({
  el: "#app",
  data() {
    return {
      filmes: null,
      filme: {
        id: null,
        titulo: null,
        genero: null,
        duracao: null,
        nota: null,
      },
      filtro: "",
    };
  },
  mounted() {
    this.listar();
  },
  methods: {
    listar() {
      axios
        .get("http://127.0.0.1:5000/filmes")
        .then((response) => (this.filmes = response.data));
      this.filtro = "";
    },

    salvar() {
      if (this.filme.id) {
        axios
          .put(`http://127.0.0.1:5000/filmes/${this.filme.id}`, this.filme)
          .then((response) => {
            alert(`Ok! Filme Alterado com Sucesso!!`);
            this.listar();
          });
      } else {
        axios
          .post("http://127.0.0.1:5000/filmes", this.filme)
          .then((response) => {
            alert(`Ok! Filme Cadastrado com Código: ${response.data.id}`);
            this.listar();
          });
      }
      this.filme = {};
    },

    editar(id) {
      axios
        .get("http://127.0.0.1:5000/filmes/" + id)
        .then((response) => (this.filme = response.data));
      this.$refs.titulo.focus();
    },

    excluir(id, titulo) {
      if (confirm(`Confirma exclusão do filme '${titulo}'?`)) {
        axios.delete("http://127.0.0.1:5000/filmes/" + id).then((response) => {
          alert(`Ok! Filme '${titulo}' excluído com sucesso!`);
          this.listar();
        });
      }
    },

    pesquisar() {
      if (this.filtro.length == 0) {
        this.listar();
      } else {
        axios
          .get(`http://127.0.0.1:5000/filmes/pesq/${this.filtro}`)
          .then((response) => (this.filmes = response.data));
      }
    },
  },
  filters: {
    formataNota(value) {
      return value.toFixed(1);
    },
    formataDuracao(value) {
      var hora = parseInt(value / 60);
      var min = value % 60;
      if (hora == 0) {
        return `${min}min`;
      } else if (min == 0) {
        return `${hora}h`;
      } else {
        return `${hora}h${min}min`;
      }
    },
  },
});
