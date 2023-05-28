import { Component } from '@angular/core';

@Component({
  selector: 'app-show',
  templateUrl: './show.component.html',
  styleUrls: ['./show.component.css']
})
export class ShowComponent {

  deleteCondition: boolean = true

  items = [
    {
      'First': 'Mark',
      'Last': 'Otto',
      'Handle': '@mdo',
  },
  {
    'First': 'Marco',
    'Last': 'Rossi',
    'Handle': '@mrssi',
}
  ]


}
