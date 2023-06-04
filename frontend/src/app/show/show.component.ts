import { Component, OnInit } from '@angular/core';
import { HttpClient }  from'@angular/common/http';
import { Router, NavigationExtras } from '@angular/router';

@Component({
  selector: 'app-show',
  templateUrl: './show.component.html',
  styleUrls: ['./show.component.css']
})
export class ShowComponent implements OnInit{

  items = []
  titlesItems = []
  activeTable = 'Esemplari'


  constructor(private httpClient : HttpClient, private router: Router){
    if (this.router.getCurrentNavigation().extras.state){
      this.activeTable = router.getCurrentNavigation().extras.state.table
    }
  }


  changeActiveTable(table){
    this.activeTable = table
    this.getData(this.activeTable)
  }


  ngOnInit(): void {
    this.getData(this.activeTable)
  }

  
  getData(table: string){
    this.items = []
    this.titlesItems = []
    this.httpClient
    .get<any>(
      `http://127.0.0.1:8080/${table.toLowerCase()}/GET`
      )
    .subscribe( {
      next: ris => {
          this.items = []
          this.titlesItems = []
          for (let key in ris[0]){
            this.titlesItems.push(key)
          }
          for (let p of ris){
            this.items.push({'ID': p?.ID, 'DataOra': p?.DataOra,'Motivo': p?.Motivo,'IDEsemplari': p?.IDEsemplari, 'NomeSpecie': p?.NomeSpecie, 'IDVasca': p?.IDVasca, 'Tipo': p?.Tipo, 'PianoTemporale': p?.PianoTemporale, 'Nome': p?.Nome, 'onlyRead': this.activeTable == 'Esemplari' ? true : false, 'deleteCondition': true})
          }
    },
      error: error => {
        console.error('Error --> ', error);
    }
  })
  }

  add_page(){
    let nav: NavigationExtras = {
      state: {
        table: this.activeTable,
        headers: this.titlesItems
      }
    }
    this.router.navigate(['add'], nav)
  }

  update_page(d){

    let nav: NavigationExtras = {
      state: {
        table: this.activeTable,
        headers: this.titlesItems,
        data: d
      }
    }
    this.router.navigate(['update'], nav)
  }


  delete_button(x, set: boolean) {
    if(!set){
      x['deleteCondition'] = set
    }else{
      this.httpClient
      .delete<any>(
        `http://127.0.0.1:8080/${this.activeTable.toLowerCase()}/DELETE?${this.activeTable == 'Specie' ? 'nome' : 'id'}=${x[(this.activeTable == 'Specie' ? 'Nome' : 'ID')]}`
        )
      .subscribe({
        next: ris => {
          console.log(ris)
          this.getData(this.activeTable)
        },
        error: error => {
          console.error('Error --> ', error);
          
      }
    }
      )
  }

}


}
