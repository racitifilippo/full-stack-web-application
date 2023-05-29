import { Component } from '@angular/core';

@Component({
  selector: 'app-show',
  templateUrl: './show.component.html',
  styleUrls: ['./show.component.css']
})
export class ShowComponent {

  //deleteCondition: boolean = true

  items = [
    {
      'id': 0,
      'First': 'Mark',
      'Last': 'Otto',
      'Handle': '@mdo',
      'deleteCondition': true
  },
  {
    'id': 1,
    'First': 'Marco',
    'Last': 'Rossi',
    'Handle': '@mrssi',
    'deleteCondition': true
}
  ]








  
delete_button(id: number, set: boolean) {
  for (let x of this.items) {
    if (x['id'] == id){
      x['deleteCondition'] = set
    }
  }
}


}
