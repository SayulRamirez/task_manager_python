import { Component } from '@angular/core';
import { DesktopToggle } from './component/desktop-toggle/desktop-toggle';

@Component({
  imports: [DesktopToggle],
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