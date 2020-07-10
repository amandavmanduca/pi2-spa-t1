new Vue({
  el: "#app",
  data() {
    return {
      controles: null,
      controle: {
        id: null,
        dia: null,
        valor: null,
        nome: null,
        descricao: null,
        classe: null,
        caixa: null,
        pagto: null,
        acao: null,
      },
      filtro: "",
      filtraData: "",
      retornaData: "",
      dados: null,
      dado: {
        
      },
      retorna: null,
    };
  },
  mounted() {


    
    //if (localStorage.filtraData) {
    //  this.filtraData = JSON.parse(localStorage.getItem('filtraData'));
    //}
  
    this.listar();
    this.listaDadosData();
    
  },
  methods: {

    //filtraDia() {
    //  localStorage.filtraData = this.filtraData;
    //},
    
    listaDadosData() {      
      if (this.filtraData.length == 0 || this.filtraData == 'global') {
        axios.get(`http://127.0.0.1:5000/dados`).then((response) => (this.dados = response.data));
        return this.dados;
      } else if (this.filtraData.length != 0 ) {
        axios.get(`http://127.0.0.1:5000/dados/${this.filtraData}`).then((response) => (this.dados = response.data));
        return this.dados;
      }
    },


    listar() {
      axios
        .get("http://127.0.0.1:5000/controles/hoje")
        .then((response) => (this.controles = response.data));
      this.filtro = "";
      this.listaDadosData()
    },

    salvar() {
      if (this.controle.id) {
        axios
          .put(`http://127.0.0.1:5000/controles/${this.controle.id}`, this.controle)
          .then((response) => {
            alert(`Ok! Dado Alterado com Sucesso!!`);
            this.listar();
            this.listaDadosData();
          });
      } else {
        axios
          .post("http://127.0.0.1:5000/controles", this.controle)
          .then((response) => {
            alert(`Ok! Dado Cadastrado com Código: ${response.data.id}`);
            this.listar();
            this.listaDadosData();
          });
      }
      this.controle = {};
      this.controle.classe = null;
      this.controle.caixa = null;
      this.controle.pagto = null;
      this.controle.acao = null;



    },

    editar(id) {
      axios
        .get("http://127.0.0.1:5000/controles/" + id)
        .then((response) => (this.controle = response.data));
      this.$refs.titulo.focus();
      this.listar();
      this.listaDadosData()
    },

    excluir(id, descricao) {
      if (confirm(`Confirma exclusão de dados: '${descricao}'?`)) {
        axios.delete("http://127.0.0.1:5000/controles/" + id).then((response) => {
          alert(`Ok! Dado '${descricao}' excluído com sucesso!`);
          this.listar();
          this.listaDadosData()
        });
      }
    },

    pesquisar() {
      if (this.filtro.length == 0) {
        this.listar();
      } else if (this.filtro == "global"){
        axios
        .get(`http://127.0.0.1:5000/controles`)
        .then((response) => (this.controles = response.data));
      } else {
        axios
          .get(`http://127.0.0.1:5000/controles/filtra/${this.filtro}`)
          .then((response) => (this.controles = response.data));
      }
    },
    limpar() {
      this.controle = {};
      this.controle.classe = null;
      this.controle.caixa = null;
      this.controle.pagto = null;
      this.controle.acao = null;
    }

    
  },
  

  filters: {


    formataNome(value) {
      var loweredText = value.toLowerCase();
      var words = loweredText.split(" ");
      for (var a = 0; a < words.length; a++) {
          var w = words[a];
  
          var firstLetter = w[0];
          w = firstLetter.toUpperCase() + w.slice(1);
  
          words[a] = w;
      }
      return words.join(" ");
      //return `${value.charAt(0).toUpperCase()}${value.slice(1)}`;
    },
    formataAcao(value){
      valor = `${value.charAt(0).toUpperCase()}`
      return valor;
    },
    formataValor(value) {
      if (value != null) {
        return value.toFixed(2);
      } else {
        return 0;
      }

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

    }
  },
});
