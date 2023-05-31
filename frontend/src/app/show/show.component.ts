import { Component, OnInit } from '@angular/core';
import { HttpClient }  from'@angular/common/http';

@Component({
  selector: 'app-show',
  templateUrl: './show.component.html',
  styleUrls: ['./show.component.css']
})
export class ShowComponent implements OnInit{

  //deleteCondition: boolean = true

  items = []
  titlesItems = []
  activeTable = 'Esemplari'

  constructor(private httpClient : HttpClient){}


  changeActiveTable(table){
    this.activeTable = table
    this.getData(this.activeTable)

  }


  ngOnInit(): void {
    this.getData(this.activeTable)
  }

  


  getData(table: string){
    this.httpClient
    .get<any>(
      "http://127.0.0.1:8080/" + table.toLowerCase() + "/GET"
      )
    .subscribe( 
      httpResponse => { 
        this.items = []
        this.titlesItems = []
        for (let key in httpResponse[0]){
          this.titlesItems.push(key)
        }
        for (let p of httpResponse){
          this.items.push({'ID': p?.ID, 'DataOra': p?.DataOra,'Motivo': p?.Motivo,'IDEsemplari': p?.IDEsemplari, 'NomeSpecie': p?.NomeSpecie, 'IDVasca': p?.IDVasca, 'Tipo': p?.Tipo, 'PianoTemporale': p?.PianoTemporale, 'Nome': p?.Nome, 'onlyRead': this.activeTable == 'Esemplari' ? true : false, 'deleteCondition': true})
        }
      }
      )
  }






  
delete_button(x, set: boolean) {
  // for (let x of this.items) {
  //   if (x['id'] == id){
  //     x['deleteCondition'] = set
  //   }
  // }
  x['deleteCondition'] = set
}


}
