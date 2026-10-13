import { Component } from '@angular/core';
import { Slide } from './slide/slide';

@Component({
  imports: [Slide],
  selector: 'app-auth',
  styleUrl: './auth.css',
  templateUrl: './auth.html',
})
export class Auth {
  isRegister = false;

  toggleAuth() {
    this.isRegister = !this.isRegister;
  }

  selectToggleAuth(isSelected: boolean) {
    this.isRegister = isSelected;
  }
}
