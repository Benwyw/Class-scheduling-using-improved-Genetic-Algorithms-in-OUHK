<html>
  <head>
    <title>Display Schedule</title>
    <link rel="stylesheet" href="/static/PSSTYLEREQ_ZHT_10.css">
    <link rel="stylesheet" href="/static/SSS_STYLESHEET_ZHT_30.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  </head>
  <script>
      $(document).ready(function() {
      $(".scheduleTable").hide();
      $('.'+$("#programmeYear").val()).show();
      $("#programmeYear").change(function() {
            $(".scheduleTable").hide();
            $('.'+$(this).val()).show();
      });
    });
  </script>
  <body>
  <h1>OUHK Course Schedules</h1>
    <form action="/display" method="post">
        <h3>Select your programme and year of study</h3>
        <p>Use the drop down box below to select your programme and year code.</p>
        <p>
        Programme and Year: 
        <select name="programmeYear" id="programmeYear">
            % for programme in oldGen:
                % for year in programme[1:]:
                    <option value={{programme[0]}}_{{year[0]}}>{{programme[0]}}_{{year[0]}}</option>
                % end
            % end
        </select>
    </form>
    %for programme in oldGen:
        %programmeName = programme[0]
        %for year in programme[1:]:
            %programmeYear = year[0]
            <div class="scheduleTable {{programmeName}}_{{programmeYear}}">
            %list9 = []
            %list11 = []
            %list14 = []
            %list16 = []
            <h2>Initial : {{programmeName}} ,Year {{programmeYear}}</h2>
            <h3>Fitness : {{ole_fitness}}</h3>
             <div>
                <table cellspacing="0" cellpadding="2" width="100%" class="PSLEVEL1GRIDNBO" id="WEEKLY_SCHED_HTMLAREA">
                    <colgroup span="1" width="9%" align="center" valign="middle"></colgroup>
                    <colgroup span="7" width="13%" align="center" valign="middle"></colgroup>
                    <tbody>
                        <tr>
                            <th scope="col" align="center" class="SSSWEEKLYA1BACKGROUND">時間</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期一</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期二</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期三</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期四</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期五</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期六</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期日</th>
                      </tr>
                      <tr>
                        <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                          <span class="SSSTEXTWEEKLYTIME">8:00AM</span>
                        </td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                      </tr>
            %for yearCourse in year[1]:
                %for lesson in yearCourse:
                    %if "09 - 11" in lesson[8]:
                        %list9.append(lesson)
                    %elif "11 - 13" in lesson[8]:
                        %list11.append(lesson)
                    %elif "14 - 16" in lesson[8]:
                        %list14.append(lesson)
                    %elif "16 - 18" in lesson[8]:
                        %list16.append(lesson)
                    %end
                %end
            %end
            %realList9  = [[],[],[],[],[]]
            %realList11 = [[],[],[],[],[]]
            %realList14 = [[],[],[],[],[]]
            %realList16 = [[],[],[],[],[]]
            %for lesson in list9:
                %if "Mon" in lesson[8]:
                    %realList9[0].append(lesson)
                %elif "Tue" in lesson[8]:
                    %realList9[1].append(lesson)
                %elif "Wed" in lesson[8]:
                    %realList9[2].append(lesson)
                %elif "Thu" in lesson[8]:
                    %realList9[3].append(lesson)
                %elif "Fri" in lesson[8]:
                    %realList9[4].append(lesson)
                %end
            %end
            %for lesson in list11:
                %if "Mon" in lesson[8]:
                    %realList11[0].append(lesson)
                %elif "Tue" in lesson[8]:
                    %realList11[1].append(lesson)
                %elif "Wed" in lesson[8]:
                    %realList11[2].append(lesson)
                %elif "Thu" in lesson[8]:
                    %realList11[3].append(lesson)
                %elif "Fri" in lesson[8]:
                    %realList11[4].append(lesson)
                %end
            %end
            %for lesson in list14:
                %if "Mon" in lesson[8]:
                    %realList14[0].append(lesson)
                %elif "Tue" in lesson[8]:
                    %realList14[1].append(lesson)
                %elif "Wed" in lesson[8]:
                    %realList14[2].append(lesson)
                %elif "Thu" in lesson[8]:
                    %realList14[3].append(lesson)
                %elif "Fri" in lesson[8]:
                    %realList14[4].append(lesson)
                %end
            %end
            %for lesson in list16:
                %if "Mon" in lesson[8]:
                    %realList16[0].append(lesson)
                %elif "Tue" in lesson[8]:
                    %realList16[1].append(lesson)
                %elif "Wed" in lesson[8]:
                    %realList16[2].append(lesson)
                %elif "Thu" in lesson[8]:
                    %realList16[3].append(lesson)
                %elif "Fri" in lesson[8]:
                    %realList16[4].append(lesson)
                %end
            %end
            <li>{{realList9}}</li>
            <li>{{realList11}}</li>
            <li>{{realList14}}</li>
            <li>{{realList16}}</li>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">9:00AM</span>
                </td>
            %counter = 0
            %for weekdayList in realList9:
                %if len(weekdayList) > 0:
                    %counter += 1
                    <td class="SSSWEEKLYBACKGROUND" rowspan="2">
                      <span class="SSSTEXTWEEKLY">
                      %for lesson in weekdayList:
                        ({{lesson[0]}},{{lesson[7]}},{{lesson[8]}})</br>
                      %end
                      </span>
                    </td>
                %else:
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            %end
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">10:00AM</span>
                </td>
                %for i in range(8-counter-1):
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            </tr>
            
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">11:00AM</span>
                </td>
            %counter = 0
            %for weekdayList in realList11:
                %if len(weekdayList) > 0:
                    %counter += 1
                    <td class="SSSWEEKLYBACKGROUND" rowspan="2">
                      <span class="SSSTEXTWEEKLY">
                      %for lesson in weekdayList:
                        ({{lesson[0]}},{{lesson[7]}},{{lesson[8]}})</br>
                      %end
                      </span>
                    </td>
                %else:
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            %end
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">12:00PM</span>
                </td>
                %for i in range(8-counter-1):
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            </tr>  
            
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">13:00PM</span>
                </td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
              
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">14:00PM</span>
                </td>
            %counter = 0
            %for weekdayList in realList14:
                %if len(weekdayList) > 0:
                    %counter += 1
                    <td class="SSSWEEKLYBACKGROUND" rowspan="2">
                      <span class="SSSTEXTWEEKLY">
                      %for lesson in weekdayList:
                        ({{lesson[0]}},{{lesson[7]}},{{lesson[8]}})</br>
                      %end
                      </span>
                    </td>
                %else:
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            %end
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">15:00PM</span>
                </td>
                %for i in range(8-counter-1):
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            </tr>
            
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">16:00PM</span>
                </td>
            %counter = 0
            %for weekdayList in realList16:
                %if len(weekdayList) > 0:
                    %counter += 1
                    <td class="SSSWEEKLYBACKGROUND" rowspan="2">
                      <span class="SSSTEXTWEEKLY">
                      %for lesson in weekdayList:
                        ({{lesson[0]}},{{lesson[7]}},{{lesson[8]}})</br>
                      %end
                      </span>
                    </td>
                %else:
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            %end
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">17:00PM</span>
                </td>
                %for i in range(8-counter-1):
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            </tr>  
             
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">18:00PM</span>
                </td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
                    </tbody>
              </table>
            </div>
        </div>
        %end 
    %end
    

    %for programme in final:
        %programmeName = programme[0]
        %for year in programme[1:]:
            %programmeYear = year[0]
            <div class="scheduleTable {{programmeName}}_{{programmeYear}}">
            %list9 = []
            %list11 = []
            %list14 = []
            %list16 = []
            <h2>Final : {{programmeName}}, Year {{programmeYear}}</h2>
            <h3>Fitness : {{final_fitness}}</h3>
             <div>
                <table cellspacing="0" cellpadding="2" width="100%" class="PSLEVEL1GRIDNBO" id="WEEKLY_SCHED_HTMLAREA">
                    <colgroup span="1" width="9%" align="center" valign="middle"></colgroup>
                    <colgroup span="7" width="13%" align="center" valign="middle"></colgroup>
                    <tbody>
                        <tr>
                            <th scope="col" align="center" class="SSSWEEKLYA1BACKGROUND">時間</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期一</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期二</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期三</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期四</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期五</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期六</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期日</th>
                      </tr>
                      <tr>
                        <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                          <span class="SSSTEXTWEEKLYTIME">8:00AM</span>
                        </td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                      </tr>
            %for yearCourse in year[1]:
                %for lesson in yearCourse:
                    %if "09 - 11" in lesson[8]:
                        %list9.append(lesson)
                    %elif "11 - 13" in lesson[8]:
                        %list11.append(lesson)
                    %elif "14 - 16" in lesson[8]:
                        %list14.append(lesson)
                    %elif "16 - 18" in lesson[8]:
                        %list16.append(lesson)
                    %end
                %end
            %end
            %realList9  = [[],[],[],[],[]]
            %realList11 = [[],[],[],[],[]]
            %realList14 = [[],[],[],[],[]]
            %realList16 = [[],[],[],[],[]]
            %for lesson in list9:
                %if "Mon" in lesson[8]:
                    %realList9[0].append(lesson)
                %elif "Tue" in lesson[8]:
                    %realList9[1].append(lesson)
                %elif "Wed" in lesson[8]:
                    %realList9[2].append(lesson)
                %elif "Thu" in lesson[8]:
                    %realList9[3].append(lesson)
                %elif "Fri" in lesson[8]:
                    %realList9[4].append(lesson)
                %end
            %end
            %for lesson in list11:
                %if "Mon" in lesson[8]:
                    %realList11[0].append(lesson)
                %elif "Tue" in lesson[8]:
                    %realList11[1].append(lesson)
                %elif "Wed" in lesson[8]:
                    %realList11[2].append(lesson)
                %elif "Thu" in lesson[8]:
                    %realList11[3].append(lesson)
                %elif "Fri" in lesson[8]:
                    %realList11[4].append(lesson)
                %end
            %end
            %for lesson in list14:
                %if "Mon" in lesson[8]:
                    %realList14[0].append(lesson)
                %elif "Tue" in lesson[8]:
                    %realList14[1].append(lesson)
                %elif "Wed" in lesson[8]:
                    %realList14[2].append(lesson)
                %elif "Thu" in lesson[8]:
                    %realList14[3].append(lesson)
                %elif "Fri" in lesson[8]:
                    %realList14[4].append(lesson)
                %end
            %end
            %for lesson in list16:
                %if "Mon" in lesson[8]:
                    %realList16[0].append(lesson)
                %elif "Tue" in lesson[8]:
                    %realList16[1].append(lesson)
                %elif "Wed" in lesson[8]:
                    %realList16[2].append(lesson)
                %elif "Thu" in lesson[8]:
                    %realList16[3].append(lesson)
                %elif "Fri" in lesson[8]:
                    %realList16[4].append(lesson)
                %end
            %end
            <li>{{realList9}}</li>
            <li>{{realList11}}</li>
            <li>{{realList14}}</li>
            <li>{{realList16}}</li>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">9:00AM</span>
                </td>
            %counter = 0
            %for weekdayList in realList9:
                %if len(weekdayList) > 0:
                    %counter += 1
                    <td class="SSSWEEKLYBACKGROUND" rowspan="2">
                      <span class="SSSTEXTWEEKLY">
                      %for lesson in weekdayList:
                        ({{lesson[0]}},{{lesson[7]}},{{lesson[8]}})</br>
                      %end
                      </span>
                    </td>
                %else:
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            %end
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">10:00AM</span>
                </td>
                %for i in range(8-counter-1):
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            </tr>
            
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">11:00AM</span>
                </td>
            %counter = 0
            %for weekdayList in realList11:
                %if len(weekdayList) > 0:
                    %counter += 1
                    <td class="SSSWEEKLYBACKGROUND" rowspan="2">
                      <span class="SSSTEXTWEEKLY">
                      %for lesson in weekdayList:
                        ({{lesson[0]}},{{lesson[7]}},{{lesson[8]}})</br>
                      %end
                      </span>
                    </td>
                %else:
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            %end
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">12:00PM</span>
                </td>
                %for i in range(8-counter-1):
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            </tr>  
            
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">13:00PM</span>
                </td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
              
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">14:00PM</span>
                </td>
            %counter = 0
            %for weekdayList in realList14:
                %if len(weekdayList) > 0:
                    %counter += 1
                    <td class="SSSWEEKLYBACKGROUND" rowspan="2">
                      <span class="SSSTEXTWEEKLY">
                      %for lesson in weekdayList:
                        ({{lesson[0]}},{{lesson[7]}},{{lesson[8]}})</br>
                      %end
                      </span>
                    </td>
                %else:
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            %end
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">15:00PM</span>
                </td>
                %for i in range(8-counter-1):
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            </tr>
            
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">16:00PM</span>
                </td>
            %counter = 0
            %for weekdayList in realList16:
                %if len(weekdayList) > 0:
                    %counter += 1
                    <td class="SSSWEEKLYBACKGROUND" rowspan="2">
                      <span class="SSSTEXTWEEKLY">
                      %for lesson in weekdayList:
                        ({{lesson[0]}},{{lesson[7]}},{{lesson[8]}})</br>
                      %end
                      </span>
                    </td>
                %else:
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            %end
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">17:00PM</span>
                </td>
                %for i in range(8-counter-1):
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            </tr>  
             
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">18:00PM</span>
                </td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
                    </tbody>
              </table>
            </div>
        </div>
        %end 
    %end

    %for programme in secondGen:
        %programmeName = programme[0]
        %for year in programme[1:]:
            %programmeYear = year[0]
            <div class="scheduleTable {{programmeName}}_{{programmeYear}}">
            %list9 = []
            %list11 = []
            %list14 = []
            %list16 = []
            <h2>Second : {{programmeName}} ,Year {{programmeYear}}</h2>
            <h3>Fitness : {{secondGen_fitness}}</h3>
             <div>
                <table cellspacing="0" cellpadding="2" width="100%" class="PSLEVEL1GRIDNBO" id="WEEKLY_SCHED_HTMLAREA">
                    <colgroup span="1" width="9%" align="center" valign="middle"></colgroup>
                    <colgroup span="7" width="13%" align="center" valign="middle"></colgroup>
                    <tbody>
                        <tr>
                            <th scope="col" align="center" class="SSSWEEKLYA1BACKGROUND">時間</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期一</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期二</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期三</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期四</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期五</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期六</th>
                            <th scope="col" align="center" class="SSSWEEKLYDAYBACKGROUND">星期日</th>
                      </tr>
                      <tr>
                        <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                          <span class="SSSTEXTWEEKLYTIME">8:00AM</span>
                        </td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                        <td class="PSLEVEL3GRID">&nbsp;</td>
                      </tr>
            %for yearCourse in year[1]:
                %for lesson in yearCourse:
                    %if "09 - 11" in lesson[8]:
                        %list9.append(lesson)
                    %elif "11 - 13" in lesson[8]:
                        %list11.append(lesson)
                    %elif "14 - 16" in lesson[8]:
                        %list14.append(lesson)
                    %elif "16 - 18" in lesson[8]:
                        %list16.append(lesson)
                    %end
                %end
            %end
            %realList9  = [[],[],[],[],[]]
            %realList11 = [[],[],[],[],[]]
            %realList14 = [[],[],[],[],[]]
            %realList16 = [[],[],[],[],[]]
            %for lesson in list9:
                %if "Mon" in lesson[8]:
                    %realList9[0].append(lesson)
                %elif "Tue" in lesson[8]:
                    %realList9[1].append(lesson)
                %elif "Wed" in lesson[8]:
                    %realList9[2].append(lesson)
                %elif "Thu" in lesson[8]:
                    %realList9[3].append(lesson)
                %elif "Fri" in lesson[8]:
                    %realList9[4].append(lesson)
                %end
            %end
            %for lesson in list11:
                %if "Mon" in lesson[8]:
                    %realList11[0].append(lesson)
                %elif "Tue" in lesson[8]:
                    %realList11[1].append(lesson)
                %elif "Wed" in lesson[8]:
                    %realList11[2].append(lesson)
                %elif "Thu" in lesson[8]:
                    %realList11[3].append(lesson)
                %elif "Fri" in lesson[8]:
                    %realList11[4].append(lesson)
                %end
            %end
            %for lesson in list14:
                %if "Mon" in lesson[8]:
                    %realList14[0].append(lesson)
                %elif "Tue" in lesson[8]:
                    %realList14[1].append(lesson)
                %elif "Wed" in lesson[8]:
                    %realList14[2].append(lesson)
                %elif "Thu" in lesson[8]:
                    %realList14[3].append(lesson)
                %elif "Fri" in lesson[8]:
                    %realList14[4].append(lesson)
                %end
            %end
            %for lesson in list16:
                %if "Mon" in lesson[8]:
                    %realList16[0].append(lesson)
                %elif "Tue" in lesson[8]:
                    %realList16[1].append(lesson)
                %elif "Wed" in lesson[8]:
                    %realList16[2].append(lesson)
                %elif "Thu" in lesson[8]:
                    %realList16[3].append(lesson)
                %elif "Fri" in lesson[8]:
                    %realList16[4].append(lesson)
                %end
            %end
            <li>{{realList9}}</li>
            <li>{{realList11}}</li>
            <li>{{realList14}}</li>
            <li>{{realList16}}</li>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">9:00AM</span>
                </td>
            %counter = 0
            %for weekdayList in realList9:
                %if len(weekdayList) > 0:
                    %counter += 1
                    <td class="SSSWEEKLYBACKGROUND" rowspan="2">
                      <span class="SSSTEXTWEEKLY">
                      %for lesson in weekdayList:
                        ({{lesson[0]}},{{lesson[7]}},{{lesson[8]}})</br>
                      %end
                      </span>
                    </td>
                %else:
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            %end
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">10:00AM</span>
                </td>
                %for i in range(8-counter-1):
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            </tr>
            
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">11:00AM</span>
                </td>
            %counter = 0
            %for weekdayList in realList11:
                %if len(weekdayList) > 0:
                    %counter += 1
                    <td class="SSSWEEKLYBACKGROUND" rowspan="2">
                      <span class="SSSTEXTWEEKLY">
                      %for lesson in weekdayList:
                        ({{lesson[0]}},{{lesson[7]}},{{lesson[8]}})</br>
                      %end
                      </span>
                    </td>
                %else:
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            %end
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">12:00PM</span>
                </td>
                %for i in range(8-counter-1):
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            </tr>  
            
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">13:00PM</span>
                </td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
              
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">14:00PM</span>
                </td>
            %counter = 0
            %for weekdayList in realList14:
                %if len(weekdayList) > 0:
                    %counter += 1
                    <td class="SSSWEEKLYBACKGROUND" rowspan="2">
                      <span class="SSSTEXTWEEKLY">
                      %for lesson in weekdayList:
                        ({{lesson[0]}},{{lesson[7]}},{{lesson[8]}})</br>
                      %end
                      </span>
                    </td>
                %else:
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            %end
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">15:00PM</span>
                </td>
                %for i in range(8-counter-1):
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            </tr>
            
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">16:00PM</span>
                </td>
            %counter = 0
            %for weekdayList in realList16:
                %if len(weekdayList) > 0:
                    %counter += 1
                    <td class="SSSWEEKLYBACKGROUND" rowspan="2">
                      <span class="SSSTEXTWEEKLY">
                      %for lesson in weekdayList:
                        ({{lesson[0]}},{{lesson[7]}},{{lesson[8]}})</br>
                      %end
                      </span>
                    </td>
                %else:
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            %end
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">17:00PM</span>
                </td>
                %for i in range(8-counter-1):
                    <td class="PSLEVEL3GRID">&nbsp;</td>
                %end
            </tr>  
             
            <tr>
                <td class="SSSWEEKLYTIMEBACKGROUND" rowspan="1">
                  <span class="SSSTEXTWEEKLYTIME">18:00PM</span>
                </td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
                <td class="PSLEVEL3GRID">&nbsp;</td>
            </tr>
                    </tbody>
              </table>
            </div>
        </div>
        %end 
    %end
  </body>
</html>
