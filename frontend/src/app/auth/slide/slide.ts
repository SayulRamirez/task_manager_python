import { Component, input, output } from '@angular/core';

@Component({
  imports: [],
  selector: 'app-slide',
  styleUrl: './slide.css',
  templateUrl: './slide.html',
})
export class Slide {
  question = input.required<string>();
  description = input.required<string>();
  titleButton = input.required<string>();
  toggleAuth = output<void>();

  onToggleAuth() {
    this.toggleAuth.emit()
  }
}
