import { Component, OnInit } from '@angular/core';
import { HttpClient }  from'@angular/common/http';
import { Router, NavigationExtras } from '@angular/router';

@Component({
  selector: 'app-add',
  templateUrl: './add.component.html',
  styleUrls: ['./add.component.css']
})
export class AddComponent {

  headers = ['DataOra', 'Motivo', 'IDEsemplari']
  activeTable: string = 'Esemplari'

  constructor(private httpClient : HttpClient, private router:Router){
    if (this.router.getCurrentNavigation().extras.state){
      this.headers = router.getCurrentNavigation().extras.state.headers
      if (this.headers.includes('ID')){
        this.headers.splice(this.headers.indexOf('ID'), 1)
      }

      this.activeTable = router.getCurrentNavigation().extras.state.table
    }
  }
  
  
  showError = false
  showSuccess = false
  
  data = {
    'ID': undefined, 
    'DataOra': undefined,
    'Motivo': undefined,
    'IDEsemplari': undefined, 
    'NomeSpecie': undefined, 
    'IDVasca': undefined, 
    'Tipo': undefined, 
    'PianoTemporale': undefined, 
    'Nome': undefined, 
    'onlyRead': this.activeTable == 'Esemplari' ? true : false, 
    'deleteCondition': true
  }
  
  home_page(){
    let nav: NavigationExtras = {
      state: {
        table: this.activeTable
      }
    }
    this.router.navigate([''], nav)
  }
  
  addData(){
    this.httpClient
    .post<any>(
      `http://127.0.0.1:8080/${this.activeTable.toLowerCase()}/POST`,
      this.data
      )
    .subscribe({
      next: ris => {
        console.log(ris)
        this.data = {
          'ID': undefined, 
          'DataOra': undefined,
          'Motivo': undefined,
          'IDEsemplari': undefined, 
          'NomeSpecie': undefined, 
          'IDVasca': undefined, 
          'Tipo': undefined, 
          'PianoTemporale': undefined, 
          'Nome': undefined, 
          'onlyRead': this.activeTable == 'Esemplari' ? true : false, 
          'deleteCondition': true
          }
        this.showSuccess = true
        this.showError = false
      },
      error: error => {
        console.error('Error --> ', error);
        this.showError = true
        this.showSuccess = false
    }
    }
    )
  }


}
    


