import { Component } from '@angular/core';
import { HttpClient }  from'@angular/common/http';
import { Router, NavigationExtras } from '@angular/router';

@Component({
  selector: 'app-update',
  templateUrl: './update.component.html',
  styleUrls: ['./update.component.css']
})
export class UpdateComponent {


  headers = ['DataOra', 'Motivo', 'IDEsemplari']
  activeTable = 'Esemplari'

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
  

  constructor(private httpClient : HttpClient, private router: Router){

    if (this.router.getCurrentNavigation().extras.state){
      this.headers = router.getCurrentNavigation().extras.state.headers
      if (this.headers.includes('ID')){
        this.headers.splice(this.headers.indexOf('ID'), 1)
      }
      if (this.headers.includes('Nome')){
        this.headers.splice(this.headers.indexOf('Nome'), 1)
      }

      this.activeTable = router.getCurrentNavigation().extras.state.table
      this.data = router.getCurrentNavigation().extras.state.data
    }

}


home_page(){
  let nav: NavigationExtras = {
    state: {
      table: this.activeTable
    }
  }
  this.router.navigate([''], nav)
}


update_data(){
  this.httpClient
  .put<any>(
    `http://127.0.0.1:8080/${this.activeTable.toLowerCase()}/PUT?${this.activeTable == 'Specie' ? "nome" : "id"}=${this.activeTable == 'Specie' ? this.data["Nome"] : this.data["ID"]}`,
    this.data
    )
  .subscribe({
    next: ris => {
      console.log(ris)
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
