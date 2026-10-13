import { Component, input, output } from '@angular/core';

@Component({
  imports: [],
  selector: 'app-mobile-toggle',
  styleUrl: './mobile-toggle.css',
  templateUrl: './mobile-toggle.html',
})
export class MobileToggle {
  message = input.required<string>();
  titleButton = input.required<string>();
  isRegister = input.required<boolean>();
  toggleAuth = output<void>();


  onToggleAuth() {
    this.toggleAuth.emit();
  }
}
