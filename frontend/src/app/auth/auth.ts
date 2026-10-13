import { Component } from '@angular/core';

@Component({
  imports: [],
  selector: 'app-auth',
  styleUrl: './auth.css',
  templateUrl: './auth.html',
})
export class Auth {
  isRegister = false;

  toggleAuth() {
    this.isRegister = !this.isRegister;
  }
}
