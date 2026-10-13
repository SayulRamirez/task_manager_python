import { Component, input, output } from '@angular/core';

@Component({
  imports: [],
  selector: 'app-desktop-toggle',
  styleUrl: './desktop-toggle.css',
  templateUrl: './desktop-toggle.html',
})
export class DesktopToggle {
  question = input.required<string>();
  description = input.required<string>();
  titleButton = input.required<string>();
  toggleAuth = output<void>();

  onToggleAuth() {
    this.toggleAuth.emit()
  }
}
