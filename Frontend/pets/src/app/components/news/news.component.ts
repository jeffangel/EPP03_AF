import { Component } from '@angular/core';

import { AuthService } from '../../services/auth.service'
import { CaseService } from '../../services/case.service'

@Component({
  selector: 'app-news',
  templateUrl: './news.component.html',
  styleUrls: ['./news.component.css']
})
export class NewsComponent {

  cases: any
  
  constructor(private authService: AuthService,
              private caseService: CaseService) { }
  
  ngOnInit(): void {
    this.authService.logged()
    this.caseService.retrieve_cases().subscribe({
      next: data => {
        this.cases = data["cases"]
        console.log(this.cases)
      },
      error: error => {
        console.error('Ocurrió un error: ', error)
      }
    })
  }

}
