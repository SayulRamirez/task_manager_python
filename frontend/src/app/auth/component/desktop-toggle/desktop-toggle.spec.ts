import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DesktopToggle } from './desktop-toggle';

describe('Slide', () => {
  let component: DesktopToggle;
  let fixture: ComponentFixture<DesktopToggle>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DesktopToggle],
    }).compileComponents();

    fixture = TestBed.createComponent(DesktopToggle);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
